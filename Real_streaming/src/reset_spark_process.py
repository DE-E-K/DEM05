"""
Reset PostgreSQL Table in Real-Time Streaming Pipeline
Clears all data from the events table and resets the streaming checkpoint.

Usage:
    python reset_spark_process.py
    
    Or with spark-submit:
    spark-submit --jars lib/postgresql-42.7.3.jar src/reset_spark_process.py
"""

import os
import sys
import logging
import shutil
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
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
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType,
)


def load_config(config_file: str) -> dict:
    """Load PostgreSQL connection details."""
    config = {}
    config_path = Path(config_file)
    
    if not config_path.exists():
        config_path = Path(__file__).parent.parent / "config" / "postgres_connection_details.txt"
    
    try:
        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    # Strip quotes if present
                    if len(value) >= 2 and ((value.startswith('"') and value.endswith('"')) or \
                                            (value.startswith("'") and value.endswith("'"))):
                        value = value[1:-1]
                    config[key] = value
        logger.info(f"Loaded config from {config_path}")
    except FileNotFoundError:
        logger.warning(f"Config file not found: {config_path}")
    
    return config


def get_spark_session(jar_path: str = None) -> SparkSession:
    """Create and return a Spark session with PostgreSQL JDBC driver."""
    if jar_path is None:
        possible_paths = [
            "postgresql-42.7.3.jar",
            os.path.join(Path(__file__).parent.parent, "lib", "postgresql-42.7.3.jar"),
            os.path.join(Path(__file__).parent, "postgresql-42.7.3.jar"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                jar_path = os.path.abspath(path)
                break
    
    if jar_path:
        logger.info(f"Using JDBC driver: {jar_path}")
        return (
            SparkSession.builder
            .appName("ResetEcommerceStreaming")
            .config("spark.jars", jar_path)
            .config("spark.driver.extraClassPath", jar_path)
            .getOrCreate()
        )
    else:
        logger.warning("PostgreSQL JDBC driver not found.")
        return SparkSession.builder.appName("ResetEcommerceStreaming").getOrCreate()


def define_schema() -> StructType:
    """Define the schema for events table."""
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


def reset_table_and_checkpoint() -> None:
    """Reset PostgreSQL table and clear checkpoint directory."""
    config = load_config("../config/postgres_connection_details.txt")
    
    spark = get_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    logger.info("=" * 60)
    logger.info("Resetting Streaming Pipeline")
    logger.info("=" * 60)
    
    db_host = config.get("host", "localhost")
    db_port = config.get("port", "5432")
    db_name = config.get("database", "ecommerce_streaming")
    db_user = config.get("user", "postgres")
    db_password = config.get("password", "")
    table_name = config.get("table", "events")
    
    jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"
    
    # Reset table
    try:
        logger.info(f"Truncating table '{table_name}'...")
        schema = define_schema()
        empty_df = spark.createDataFrame([], schema)
        
        empty_df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", table_name) \
            .option("user", db_user) \
            .option("password", db_password) \
            .option("driver", "org.postgresql.Driver") \
            .option("truncate", "true") \
            .mode("overwrite") \
            .save()
        
        logger.info(f"✓ Table '{table_name}' truncated successfully.")
    except Exception as e:
        logger.error(f"✗ Failed to truncate table: {e}", exc_info=True)
    
    # Clear checkpoint
    checkpoint_dir = Path(__file__).parent.parent / "data" / "checkpoint"
    if checkpoint_dir.exists():
        try:
            shutil.rmtree(checkpoint_dir)
            logger.info(f"✓ Cleared checkpoint directory: {checkpoint_dir}")
        except Exception as e:
            logger.warning(f"Could not remove checkpoint directory: {e}")
    
    spark.stop()
    logger.info("=" * 60)
    logger.info("Reset completed.")


if __name__ == "__main__":
    reset_table_and_checkpoint()
