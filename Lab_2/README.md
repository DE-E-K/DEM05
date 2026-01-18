# Lab 2: Real-Time Flight Data Streaming

An end-to-end streaming data pipeline that ingests flight events, processes them with Spark Structured Streaming, and persists them to PostgreSQL.

## \U0001f4c2 Project Structure
```text
Lab_2/
├── config/                # Database setup and connection details
│   ├── postgres_setup.sql
│   └── .env
├── data/                  # Input data landing zone
├── docs/                  # Documentation & Diagrams
│   ├── system_architecture.png
│   ├── user_guide.md
│   └── project_overview.md
├── lib/                   # JDBC Drivers (postgresql.jar)
└── src/                   # Python Source Code
    ├── data_generator.py  # Synthetic Data Producer
    └── spark_streaming_to_postgres.py # Main Consumer
```

## Documentation
*   **[User Guide](./docs/user_guide.md)**: detailed setup and execution instructions.
*   **[Project Overview](./docs/project_overview.md)**: High-level architectural context.
*   **[Walkthrough](./docs/walkthrough.md)**: Step-by-step verification process.

## Quick Start
1.  **Setup Database**: Run `config/postgres_setup.sql`.
2.  **Generate Data**: `python src/data_generator.py`
3.  **Start Stream**: `spark-submit ... src/spark_streaming_to_postgres.py`
    *(See User Guide for full start command)*
