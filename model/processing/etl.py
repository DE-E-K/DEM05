from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, explode, when, size, concat_ws, lit, to_date, year, regexp_replace, expr
)
from model.config import (
    SPARK_APP_NAME, SPARK_MASTER, 
    RAW_DATA_PATH, PROCESSED_DATA_PATH
)
from model.processing.schemas import raw_movie_schema
from model.config import COLUMNS_TO_DROP, FINAL_COLUMNS_ORDER
from model.logger import get_logger

import os
import sys

logger = get_logger(__name__)

def create_spark_session():
    """Confgiures and returns a SparkSession."""
    # Workaround for Windows missing HADOOP_HOME
    if sys.platform == "win32":
        # Check if user provided path exists, otherwise fall back or warn
        hadoop_home = "C:/hadoop"
        os.environ["HADOOP_HOME"] = hadoop_home
        
        # CRITICAL: Add bin to PATH so Spark can find winutils.exe
        if f"{hadoop_home}/bin" not in os.environ["PATH"].replace("\\", "/"):
             os.environ["PATH"] = f"{hadoop_home}/bin;" + os.environ["PATH"]
             
        if not os.path.exists("C:/hadoop/bin/winutils.exe"):
            logger.warning("winutils.exe not found at C:/hadoop/bin/winutils.exe. Spark Write may fail.")
    
    return SparkSession.builder \
        .appName(SPARK_APP_NAME) \
        .master(SPARK_MASTER) \
        .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
        .config("spark.hadoop.io.native.lib.available", "false") \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
        .getOrCreate()

def run_etl():
    """Main ETL workflow: Load raw JSON -> Transform -> Write Parquet."""
    spark = create_spark_session()
    logger.info("Spark Session created.")

    # ===== 1. READ =====
    import glob
    raw_path_str = str(RAW_DATA_PATH / "*.json")
    files = [f.replace("\\", "/") for f in glob.glob(raw_path_str)]
    
    if not files:
        logger.error(f"No JSON files found in {raw_path_str}")
        spark.stop()
        return

    logger.info(f"Reading {len(files)} files via explicit list.")
    
    # Force schema enforcement
    df_raw = spark.read.schema(raw_movie_schema).json(files)
    logger.info(f"Raw data loaded: {df_raw.count()} records")

    # ===== 2. CLEAN & TRANSFORM =====
    logger.info("Starting transformations...")
    
    df_transformed = (df_raw 
        # A. Filter & Basic Clean
        .filter(col("status") == "Released") 
        .filter(col("release_date").isNotNull()) 
        .drop(*COLUMNS_TO_DROP)
        
        # B. Formatting: Dates
        .withColumn("release_date_dt", to_date(col("release_date"), "yyyy-MM-dd")) 
        .withColumn("release_year", year(col("release_date_dt"))) 
        
        # C. Cleaning: Budget/Revenue (0 -> Null, then Convert to Millions)
        .withColumn("budget", when(col("budget") == 0, None).otherwise(col("budget"))) 
        .withColumn("revenue", when(col("revenue") == 0, None).otherwise(col("revenue")))
        .withColumn("budget_musd", col("budget") / lit(1000000)) 
        .withColumn("revenue_musd", col("revenue") / lit(1000000)) 
        
        # D. Flattening & Formatting Strings (Pipe Separated)
        .withColumn("genres", expr("transform(genres, x -> x.name)")) 
        .withColumn("genres", concat_ws("|", col("genres"))) 
        
        .withColumn("production_companies", expr("transform(production_companies, x -> x.name)")) 
        .withColumn("production_companies", concat_ws("|", col("production_companies"))) 
        
        .withColumn("production_countries", expr("transform(production_countries, x -> x.name)")) 
        .withColumn("production_countries", concat_ws("|", col("production_countries"))) 
        
        .withColumn("spoken_languages", expr("transform(spoken_languages, x -> x.name)")) 
        .withColumn("spoken_languages", concat_ws("|", col("spoken_languages"))) 
        
        # E. Extract Complex Objects
        .withColumn("belongs_to_collection", col("belongs_to_collection.name"))
        
        # F. Calculated Columns
        .withColumn("cast_size", size(col("credits.cast"))) 
        .withColumn("crew_size", size(col("credits.crew"))) 
        
        # Extract Director: Safely extract first director, default to 'Unknown' if none
        .withColumn("director", 
            expr("coalesce(element_at(filter(credits.crew, x -> x.job == 'Director'), 1).name, 'Unknown')"))
        
        # Extract Cast: Pipe-separated list of actor names
        .withColumn("cast", expr("transform(credits.cast, x -> x.name)"))
        .withColumn("cast", concat_ws("|", col("cast")))
        
        # G. KPIs (Profit/ROI)
        .withColumn("profit", col("revenue") - col("budget"))
        .withColumn("roi", when(col("budget") > 0, col("revenue") / col("budget")).otherwise(None))
        
        # H. Drop the credits column (no longer needed, extracted into scalar columns)
        .drop("credits", "release_date_dt")
    )

    # ===== 3. FINAL SELECT & REORDER =====
    final_df = df_transformed.select(
        *[col(c) for c in FINAL_COLUMNS_ORDER],
        col("release_year")  # Keep for partitioning
    )

    logger.info(f"Transformed data ready: {final_df.count()} records")

    # ===== 4. WRITE =====
    output_path = str(PROCESSED_DATA_PATH).replace("\\", "/")
    logger.info(f"Writing processed data to: {output_path}")
    
    try:
        # Try native Spark write first
        logger.info("Attempting native Spark write...")
        final_df.write \
            .mode("overwrite") \
            .partitionBy("release_year") \
            .parquet(output_path)
            
        logger.info("Successfully wrote data using native Spark Parquet writer.")
    except Exception as e:
        logger.warning(f"Spark native write failed: {e}")
        logger.info("Falling back to Pandas/PyArrow workaround...")
        
        try:
            # Fallback: Pandas/PyArrow for Windows compatibility
            pdf = final_df.toPandas()
            import pyarrow as pa
            import pyarrow.parquet as pq
            
            table = pa.Table.from_pandas(pdf)
            pq.write_to_dataset(table, root_path=output_path, partition_cols=['release_year'])
            logger.info("Successfully wrote data using Pandas/PyArrow fallback.")
        except Exception as e2:
            logger.error(f"Both write methods failed: {e2}")
            raise e2
        
    logger.info("ETL Job Finished Successfully.")
    spark.stop()


if __name__ == "__main__":
    run_etl()
