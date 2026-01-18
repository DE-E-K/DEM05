# Lab 1: TMDB Movie Analysis

A comparative data engineering study implementing the same analytical pipeline using **Pandas** and **Apache Spark**.

## \U0001f4c2 Project Structure
```text
Lab_1/
├── data/                  # Raw and processed datasets (CSV/Parquet)
├── src/
│   ├── pandas_impl/       # Python Pandas Implementation
│   │   ├── tmdb_analysis.ipynb
│   │   └── final_report.md
│   └── spark_impl/        # PySpark Implementation
│       ├── main.py        # ETL Pipeline Entrypoint
│       ├── analysis/      # KPI Logic
│       ├── extraction/    # Data Loading
│       └── cleaning/      # Schema Enforcement
└── README.md
```

## Implementations

### 1. [Pandas Implementation](./src/pandas_impl)
*   **Best for**: Single-node processing, EDA, and quick prototyping.
*   **Key Files**: `tmdb_analysis.ipynb`

### 2. [Spark Implementation](./src/spark_impl)
*   **Best for**: Scalable distributed processing and uniform schema enforcement.
*   **Key Files**: `main.py`, `run_pipeline.ps1`, `tmdb_spark_analysis.ipynb`

## Running the Project
Navigate to the respective implementation folder and follow the inner `README.md` instructions.
