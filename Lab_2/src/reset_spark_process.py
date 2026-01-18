import sys
import os

# Unset SPARK_HOME to avoid conflict with system installation (fixes UnixStreamServer error on Windows)
if 'SPARK_HOME' in os.environ:
    del os.environ['SPARK_HOME']

# Ensure Spark workers use the same Python executable
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Set HADOOP_HOME to the user's local existing installation
if 'HADOOP_HOME' not in os.environ:
    os.environ['HADOOP_HOME'] = r'C:\hadoop'

# Ensure hadoop/bin is in PATH so Spark can find winutils.exe
hadoop_bin = os.path.join(os.environ['HADOOP_HOME'], 'bin')
if hadoop_bin not in os.environ['PATH']:
    os.environ['PATH'] += ';' + hadoop_bin

# Load connection details
def load_config(config_file):
    config = {}
    try:
        with open(config_file, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    except FileNotFoundError:
        print(f"Config file {config_file} not found. Using defaults.")
    return config

CONFIG_FILE = 'postgres_connection_details.txt'
if not os.path.exists(CONFIG_FILE):
    # Try looking in the current directory if run from elsewhere
    current_dir = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(current_dir, 'postgres_connection_details.txt')

config = load_config(CONFIG_FILE)

DB_HOST = config.get('HOST', 'localhost')
DB_PORT = config.get('PORT', '5432')
DB_NAME = config.get('DB_NAME', 'e-commerce')
DB_USER = config.get('USER', 'postgres')
DB_PASSWORD = config.get('PASSWORD', 'LearnStreaming!2026')
TABLE_NAME = config.get('TABLE_NAME', 'e_commerce_events')
JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_spark_session():
    # Assume jar is in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    jar_path = os.path.join(current_dir, "postgresql-42.7.3.jar")
    
    return SparkSession.builder \
        .appName("ResetEcommerceData") \
        .config("spark.jars", jar_path) \
        .config("spark.driver.extraClassPath", jar_path) \
        .getOrCreate()

def reset_table():
    print(f"Resetting table '{TABLE_NAME}' in database '{DB_NAME}'...")
    spark = get_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    # Define Schema (matching the standard flow)
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_timestamp", TimestampType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("price", DoubleType(), True)
    ])
    
    # Create empty DataFrame
    df = spark.createDataFrame([], schema)
    
    try:
        # We use mode "overwrite" with option "truncate" -> "true". 
        # This attempts to truncate the table. If truncate fails or isn't supported, 
        # it might drop and recreate (overwrite behavior).
        df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", TABLE_NAME) \
            .option("user", DB_USER) \
            .option("password", DB_PASSWORD) \
            .option("driver", "org.postgresql.Driver") \
            .mode("overwrite") \
            .option("truncate", "true") \
            .save()
        print(f"Successfully reset table '{TABLE_NAME}'.")
    except Exception as e:
        print(f"Error resetting table: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    reset_table()
