# User Guide

## Prerequisites
- Apache Spark installed and configured.
- PostgreSQL installed and running.
- Python 3.x installed.
- PostgreSQL JDBC Driver (e.g., `postgresql-42.x.x.jar`) available to Spark.

## Setup

1.  **Database Configuration**:
    - Update `postgres_connection_details.txt` with your database credentials.
    - Run the setup script to create the table:
      ```bash
      psql -h <host> -U <username> -d <dbname> -f postgres_setup.sql
      ```

2.  **Environment Setup**:
    - Ensure your `spark_streaming_to_postgres.py` script points to the correct input directory where CSVs will be generated.
    - Ensure the `input_data` directory exists or let the script create it.

## Running the Pipeline

1.  **Start the Data Generator**:
    Open a terminal and run:
    ```bash
    python data_generator.py
    ```
    This will start creating CSV files in the `input_data` folder.

2.  **Start the Spark Streaming Job**:
    Open another terminal and submit the Spark job (ensure you provide the path to the Postgres JDBC jar):
    ```bash
    spark-submit --packages org.postgresql:postgresql:42.5.0 spark_streaming_to_postgres.py
    ```
    *Note: If you have downloaded the jar locally, use `--jars /path/to/postgresql-42.x.x.jar` instead of `--packages`.*

3.  **Verify Data**:
    Connect to your PostgreSQL database and query the table:
    ```sql
    SELECT
        event_id,
        event_timestamp::timestamp AS event_timestamp,
        event_type
    FROM e_commerce_events
    ORDER BY event_timestamp DESC
    LIMIT 20;
    ```
    You should see rows appearing in real-time.
