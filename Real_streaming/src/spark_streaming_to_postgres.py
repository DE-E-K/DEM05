"""
Spark Structured Streaming to PostgreSQL
Reads CSV files from a directory, processes them, and writes to PostgreSQL.

Prerequisites:
    - Spark 3.0+
    - PostgreSQL JDBC driver in lib/ or same directory

Usage:
    spark-submit --jars lib/postgresql-42.7.3.jar src/spark_streaming_to_postgres.py
    
    Or with driver class path:
    spark-submit --driver-class-path lib/postgresql-42.7.3.jar \\
                 --jars lib/postgresql-42.7.3.jar \\
                 src/spark_streaming_to_postgres.py
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Set up Hadoop for Windows (if needed)
if sys.platform.startswith("win"):
    if "HADOOP_HOME" not in os.environ:
        os.environ["HADOOP_HOME"] = r"C:\hadoop"
    hadoop_bin = os.path.join(os.environ.get("HADOOP_HOME", ""), "bin")
    if hadoop_bin and hadoop_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = hadoop_bin + ";" + os.environ.get("PATH", "")

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType,
)


def load_config(config_file: str) -> dict:
    """
    Load PostgreSQL connection details from config file.
    
    Config file format:
        host=localhost
        port=5432
        database=ecommerce_streaming
        user=postgres
        password=secret
        table=events
    """
    config = {}
    config_path = Path(config_file)
    
    if not config_path.exists():
        # Try relative to current script
        config_path = Path(__file__).resolve().parent.parent / "config" / "postgres_connection_details.txt"
    
    try:
        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    config[key.strip().lower()] = value.strip()
                    key = key.strip().lower()
                    value = value.strip()
                    # Strip quotes if present (common issue with config files)
                    if len(value) >= 2 and ((value.startswith('"') and value.endswith('"')) or \
                                            (value.startswith("'") and value.endswith("'"))):
                        value = value[1:-1]
                    config[key] = value
        logger.info(f"Loaded config from {config_path}")
        # Log loaded configuration (masking password)
        safe_config = {k: '******' if 'password' in k else v for k, v in config.items()}
        logger.info(f"Active Configuration: {safe_config}")
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}. Please ensure configuration exists.")
    
    return config


def get_spark_session(jar_path: str = None) -> SparkSession:
    """Create and return a Spark session with PostgreSQL JDBC driver."""
    if jar_path is None:
        # Look for JAR in multiple locations
        possible_paths = [
            "postgresql-42.7.3.jar",
            str(Path(__file__).resolve().parent.parent / "lib" / "postgresql-42.7.3.jar"),
            str(Path(__file__).resolve().parent / "postgresql-42.7.3.jar"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                jar_path = os.path.abspath(path)
                break
    
    if jar_path:
        logger.info(f"Using JDBC driver: {jar_path}")
        return (
            SparkSession.builder
            .appName("RealTimeEcommerceStreaming")
            .config("spark.jars", jar_path)
            .config("spark.driver.extraClassPath", jar_path)
            .config("spark.sql.shuffle.partitions", "8")
            .config("spark.default.parallelism", "8")
            .getOrCreate()
        )
    else:
        logger.warning("PostgreSQL JDBC driver not found. Continuing without explicit JAR.")
        return (
            SparkSession.builder
            .appName("RealTimeEcommerceStreaming")
            .config("spark.sql.shuffle.partitions", "8")
            .getOrCreate()
        )


def define_schema() -> StructType:
    """Define the schema for incoming CSV events."""
    return StructType(
        [
            StructField("event_id", StringType(), True),
            StructField("event_type", StringType(), True),
            StructField("product_id", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("event_timestamp", TimestampType(), True),
            StructField("quantity", IntegerType(), True),
            StructField("price", DoubleType(), True),
        ]
    )


def write_to_postgres(df, epoch_id: int, config: dict) -> None:
    """
    Write a batch of data to PostgreSQL.
    
    Args:
        df: DataFrame to write
        epoch_id: Batch ID
        config: Database configuration dictionary
    """
    logger.info(f"Batch {epoch_id}: Starting batch processing.")
    if df.rdd.isEmpty():
        logger.info(f"Batch {epoch_id}: No records to write. Waiting for new data...")
        logger.info(f"Batch {epoch_id}: Finished batch (no data).")
        return
    
    db_host = config.get("host", "localhost")
    db_port = int(config.get("port", "5432"))
    db_name = config.get("database", "ecommerce_streaming")
    db_user = config.get("user", "postgres")
    db_password = config.get("password", "")
    table_name = config.get("table", "events")
    
    jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"
    
    # Persist to memory and disk for large batches
    from pyspark import StorageLevel
    df.persist(StorageLevel.MEMORY_AND_DISK)
    
    try:
        logger.info(f"Batch {epoch_id}: Writing records to {table_name}...")
        df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", db_user) \
            .option("password", db_password) \
            .option("driver", "org.postgresql.Driver") \
            .option("batchsize", "5000") \
            .mode("append") \
            .save()
        count = df.count()
        logger.info(f"Batch {epoch_id}: Successfully wrote {count} records.")
        logger.info(f"Batch {epoch_id}: Finished batch processing.")
    except Exception as e:
        logger.error(f"Batch {epoch_id}: Failed to write to database: {e}", exc_info=True)
        logger.info(f"Batch {epoch_id}: Finished batch with error.")
        raise
    finally:
        df.unpersist()


def main():
    """Main Spark Streaming job."""
    # Load configuration
    project_root = Path(__file__).resolve().parent.parent
    config_file = project_root / "config" / "postgres_connection_details.txt"
    config = load_config(str(config_file))
    
    if not config:
        logger.error("Critical configuration missing. Exiting.")
        sys.exit(1)
    
    # Create Spark session
    spark = get_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    logger.info("Real-Time E-Commerce Streaming Pipeline")
    logger.info("=" * 60)
    
    # Define schema
    schema = define_schema()
    
    # Input directory - calculate from project root
    input_dir = project_root / "data" / "input_data"
    input_dir.mkdir(parents=True, exist_ok=True)
    # Use absolute path string for Spark (works better with spaces/special chars)
    input_dir_str = str(input_dir.absolute())
    logger.info(f"Monitoring directory: {input_dir_str}")
    logger.info(f"Database: {config.get('database', 'ecommerce_streaming')}")
    logger.info(f"Table: {config.get('table', 'events')}")
    logger.info("=" * 60)
    
    try:
        # Read streaming CSV files
        streaming_df = (
            spark.readStream
            .option("header", "true")
            .option("maxFilesPerTrigger", "1")
            .option("latestFirst", "true")
            .schema(schema)
            .csv(input_dir_str)
        )
        
        # Transformations: filter nulls, deduplicate, ensure timestamp is valid
        processed_df = (
            streaming_df
            .filter(col("event_id").isNotNull())
            .filter(col("event_timestamp").isNotNull())
            .dropDuplicates(["event_id"])
        )
        
        # Write to PostgreSQL
        checkpoint_dir = str((project_root / "data" / "checkpoint").absolute())
        query = (
            processed_df.writeStream
            .foreachBatch(lambda df, epoch_id: write_to_postgres(df, epoch_id, config))
            .outputMode("append")
            .option("checkpointLocation", checkpoint_dir)
            .start()
        )
        
        logger.info("Streaming query started. Waiting for termination...")
        query.awaitTermination()
    
    except Exception as e:
        logger.error(f"Fatal error in streaming job: {e}", exc_info=True)
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
