# Walkthrough: E-commerce Real-Time Data Ingestion

This guide walks you through setting up and running the Spark Structured Streaming pipeline to ingest e-commerce events into PostgreSQL.

## Prerequisites

-   **Python 3.8+**
-   **Apache Spark 3.x**
-   **PostgreSQL**
-   **Java 8 or 11** (for Spark)

## 1. Environment Setup

### 1.1. Database Setup
Ensure PostgreSQL is running and you have created the database and table.

```bash
# Run the SQL setup script (you can copy the content to pgAdmin or run via psql)
# This creates the 'e_commerce' database and 'e_commerce_events' table.
postgres_setup.sql
```

**Verification:** Connect to the `e_commerce` database and check that `e_commerce_events` exists.

### 1.2. Python Dependencies
Ensure required libraries are installed.

```bash
pip install pyspark psycopg2-binary
```

### 1.3. Configuration
Check `postgres_connection_details.txt` to match your local PostgreSQL credentials.

```properties
HOST=localhost
PORT=5432
DB_NAME=e_commerce
USER=postgres
PASSWORD=LearnStreaming!2026
TABLE_NAME=e_commerce_events
```

## 2. Running the Pipeline

The pipeline consists of two parts: the **Data Generator** and the **Spark Streaming Job**.

### 2.1. Start the Data Generator
Open a terminal and run the generator. This script creates random CSV files in the `input_data/` directory.

```bash
python data_generator.py
```
*Leave this terminal running.*

### 2.2. Start Spark Streaming
Open a **new** terminal window and run the Spark job.

```bash
python spark_streaming_to_postgres.py
```

You should see output indicating batches are being processed:
```text
Writing batch 0 to PostgreSQL db name e_commerce table name e_commerce_events ...
Batch 0 written successfully.
```

## 3. Verification

To verify that data is arriving in PostgreSQL, run the following SQL query:

```sql
SELECT
    event_id,
    event_timestamp,
    event_type,
    product_id
FROM e_commerce_events
ORDER BY event_timestamp DESC
LIMIT 10;
```

You should see new rows appearing as the generator creates more files.

## 4. Troubleshooting

-   **Error: `java.lang.ClassNotFoundException: org.postgresql.Driver`**
    -   Ensure `postgresql-42.7.3.jar` is in the same directory as your script.
-   **Error: `Connection refused`**
    -   Check if PostgreSQL is running and the credentials in `postgres_connection_details.txt` are correct.
-   **No data in table**
    -   Check if `data_generator.py` is actually creating files in `input_data/`.
    -   Check Spark console for any error messages in the output.

## 5. Resetting the Environment

To clear the database table and start fresh:

```bash
python reset_spark_process.py
```
