import sys
import os

# Set HADOOP_HOME to the user's local existing installation
if 'HADOOP_HOME' not in os.environ:
    os.environ['HADOOP_HOME'] = r'C:\hadoop'

# Ensure hadoop/bin is in PATH so Spark can find winutils.exe
hadoop_bin = os.path.join(os.environ['HADOOP_HOME'], 'bin')
if hadoop_bin not in os.environ['PATH']:
    os.environ['PATH'] += ';' + hadoop_bin
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType


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
config = load_config(CONFIG_FILE)

# Database Configuration (Defaults or from config file)
DB_HOST = config.get('HOST', 'localhost')
DB_PORT = config.get('PORT', '5432')
DB_NAME = config.get('DB_NAME', 'e-commerce')
DB_USER = config.get('USER', 'postgres')
DB_PASSWORD = config.get('PASSWORD', 'LearnStreaming!2026')
TABLE_NAME = config.get('TABLE_NAME', 'e_commerce_events')
INPUT_DIR = 'input_data'

JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_spark_session():
    # Path to the downloaded JAR
    jar_path = os.path.abspath("postgresql-42.7.3.jar")
    return SparkSession.builder \
        .appName("EcommerceDataIngestion") \
        .config("spark.jars", jar_path) \
        .config("spark.driver.extraClassPath", jar_path) \
        .getOrCreate()

def write_to_postgres(df, epoch_id):
    print(f"Writing batch {epoch_id} to PostgreSQL db name {DB_NAME} table name {TABLE_NAME} ...")
    df.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", TABLE_NAME) \
        .option("user", DB_USER) \
        .option("password", DB_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    print(f"Batch {epoch_id} written successfully.")

def main():
    spark = get_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    # Define Schema matching the CSV header
    # event_id, event_type, product_id, user_id, event_timestamp, quantity, price
    schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_timestamp", TimestampType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("price", DoubleType(), True)
    ])

    print(f"Monitoring directory: {INPUT_DIR}")

    # Read Stream
    # Note: timestamps in CSV are strings, Spark can infer or we cast. 
    # Since we defined TimestampType in schema, Spark will try to parse. 
    # Ideally standard format yyyy-MM-dd HH:mm:ss works.
    streaming_df = spark.readStream \
        .option("header", "true") \
        .schema(schema) \
        .csv(INPUT_DIR)

    # Simple transformation (e.g., filter or just pass through)
    # Let's ensure non-null event_ids just in case or filter valid events
    clean_df = streaming_df.filter(col("event_id").isNotNull())

    # Write Stream
    query = clean_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
