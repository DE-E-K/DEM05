# User Guide

## Prerequisites
- Apache Spark installed and configured.
- PostgreSQL installed and running.
- Python 3.x installed.
- PostgreSQL JDBC Driver (e.g., `postgresql-42.x.x.jar`) available to Spark.

## Setup

1.  **Database Configuration**:
    - Update `config/postgres_connection_details.txt` with your database credentials.
    - Run the setup script to create the table:
      ```bash
      psql -h <host> -U <username> -d <dbname> -f config/postgres_setup.sql
      ```

2.  **Environment Setup**:
    - Ensure your `src/spark_streaming_to_postgres.py` script points to the correct input directory (`data/input_data`).

## Running the Pipeline

1.  **Start the Data Generator**:
    Open a terminal in `Lab_2` and run:
    ```bash
    python src/data_generator.py
    ```
    This will start creating CSV files in the `data/input_data` folder.

2.  **Start the Spark Streaming Job**:
    Open another terminal and submit the Spark job:
    ```bash
    spark-submit --driver-class-path lib/postgresql-42.7.3.jar --jars lib/postgresql-42.7.3.jar src/spark_streaming_to_postgres.py
    ```
    *Note: The command assumes you are in the `Lab_2` directory.*

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
