# Real-Time Streaming Project - Folder Structure

This document describes the organization and purpose of each directory and file in the project.

## Directory Tree

```
Real_streaming/
│
├── README.md                                   # Project overview and quick start
├── requirements.txt                            # Project dependencies
│
├── src/                                        # Source code - all application scripts
│   ├── data_generator.py                       # E-commerce event simulator
│   ├── spark_streaming_to_postgres.py          # Main Spark streaming job
│   ├── reset_spark_process.py                  # Utility to reset database/checkpoint
│   └── requirements.txt                        # Python package dependencies
│
├── data/                                       # Data storage and processing
│   ├── input_data/                             # CSV input directory (generated)
│   │   ├── events_1707370245_0.csv             # CSV file example 1
│   │   ├── events_1707370248_1.csv             # CSV file example 2
│   │   └── events_170737025X_N.csv             # Pattern: events_<timestamp>_<index>.csv
│   │
│   ├── checkpoint/                             # Spark checkpoint directory (auto-created)
│   │   ├── metadata/                           # Checkpoint metadata
│   │   └── offsets/                            # Offset tracking for fault tolerance
│   │
│   └── [logs]/                                 # Optional: application logs
│
├── config/                                     # Configuration files
│   ├── postgres_setup.sql                      # Database DDL script (CREATE TABLE, indexes)
│   └── postgres_connection_details.txt         # PostgreSQL credentials and connection info
│
├── lib/                                        # External libraries
│   └── postgresql-42.7.3.jar                   # PostgreSQL JDBC driver for Spark
│
├── docs/                                       # Documentation (this is the core)
│   ├── project_overview.md                     # High-level project description
│   ├── user_guide.md                           # Setup & execution instructions
│   ├── test_cases.md                           # Manual test plan (16 test cases)
│   ├── performance_metrics.md                  # Performance benchmarks & analysis
│   ├── system_architecture.txt                 # Detailed architecture & design
│   ├── walkthrough.md                          # Step-by-step walkthrough for first-timers
│   └── folder_structure.md                     # This file - directory guide
│
├── tests/                                     # Test scripts and test data
│   ├── [test_data_generator.py]               # Unit tests for data generator (future)
│   ├── [test_spark_job.py]                    # Integration tests (future)
│   └── [test_database.sql]                    # Database validation queries (future)
│
└── .gitignore                                   # Git ignore rules (recommended)
    └── (Should exclude: data/input_data/*, data/checkpoint/*, *.log)
```

---

## Directory Descriptions

### [Source Code](src/)

**Purpose**: Contains all runnable Python scripts for the pipeline.

**Files**:

| File | Size | Purpose | Run Command |
|------|------|---------|------------|
| `data_generator.py` | ~6 KB | Generates fake CSV event files | `python src/data_generator.py` |
| `spark_streaming_to_postgres.py` | ~8 KB | Spark Structured Streaming job | `spark-submit ...src/spark_streaming_to_postgres.py` |
| `reset_spark_process.py` | ~5 KB | Clears database & checkpoint | `python src/reset_spark_process.py` |
| `requirements.txt` | <1 KB | Python package list | `pip install -r requirements.txt` |

**Key Notes**:
- All Python scripts are production-ready with error handling and logging
- Can be run from project root: `python src/data_generator.py`
- JDBC driver location is auto-detected (looks in lib/ first, then current dir)

---

### [Data Storage](data/)

**Purpose**: Input data directory, checkpoint state, and logs.

**Subdirectories**:

#### [data/input_data](data/input_data/)
- **Purpose**: CSV files created by data_generator.py, monitored by Spark
- **File Pattern**: `events_<unix_timestamp>_<index>.csv`
- **Example**: `events_1707370245_0.csv`
- **Typical Size**: 5-50 KB per file
- **Cleanup**: Safe to delete when pipeline is stopped (will regenerate)
- **Spark Behavior**: Automatically processes new files every 30 seconds

#### [data checkpoint](data/checkpoint/)
- **Purpose**: Spark streaming state and checkpoint data
- **Auto-Created**: When Spark job starts
- **Content**: Offset tracking, metadata, batch information
- **Critical**: Do NOT manually edit. Use [reset_spark_process.py](reset_spark_process.py) to clear.
- **Size**: Grows slowly (~100 KB per batch)
- **Recovery**: On restart, Spark resumes from last checkpoint

#### [logs (optional)](data/logs/)
- Can place custom logs here if redirecting output
- Example: `python src/data_generator.py > data/logs/generator.log 2>&1`

---

### [Configuration](config/)

**Purpose**: Database setup and connection credentials.

**Files**:

#### `postgres_setup.sql` 
- **Purpose**: DDL script to create database, table, and indexes
- **How to Use**: `psql -U postgres -f config/postgres_setup.sql`
- **Contains**:
  - `CREATE DATABASE ecommerce_streaming`
  - `CREATE TABLE events` (7 columns)
  - `CREATE INDEX` (4 indexes for query optimization)
  - `GRANT` permissions to postgres user
- **Important**: Run once before first pipeline execution

#### [postgres connection details](config/postgres_connection_details.txt) (6 lines)
- **Purpose**: Database credentials and connection parameters
- **Format**: `key=value` pairs
- **Contents**:
  ```
  host=localhost
  port=5432
  database=ecommerce_streaming
  user=postgres
  password=your_password_here
  table=events
  ```
- **Security**: ⚠️ Contains password - keep secure, don't commit to GitHub
- **Production**: Replace with environment variables or secrets manager

---

### [External Libraries](lib/)

**Purpose**: Third-party JAR files needed by Spark.

**Files**:

#### `postgresql-42.7.3.jar`
- **Purpose**: PostgreSQL JDBC driver
- **Needed By**: Spark streaming job (writes to PostgreSQL)
- **How to Get**: Download from https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
- **Where to Place**: `lib/[this file]`
- **Spark Discovery**: Auto-detected via `--jars lib/postgresql-42.7.3.jar` in spark-submit


### [Documentation](docs/)

**Purpose**: Comprehensive documentation for understanding, using, and extending the project.

**Files** (in reading order):

| File | Audience | Length | Purpose |
|------|----------|--------|---------|
| project overview](docs/project_overview.md) | Everyone | ~100 lines | Executive summary, architecture overview, features |
| [user guide](docs/user_guide.md) | Everyone **Start here** | ~400 lines | Installation, configuration, running, troubleshooting |
| [walkthrough](docs/walkthrough.md) | First-timers | ~300 lines | Step-by-step walkthrough with expected outputs |
| [test cases](docs/test_cases.md) | EveryoneQA/Testers | ~350 lines | 16 manual test cases with pass criteria |
| [performance metrics](docs/performance_metrics.md) | Ops/Data Eng | ~400 lines | Benchmarks, bottlenecks, optimization tips |
| [system architecture](docs/system_architecture.txt) | Architects/Devs | ~500 lines | Detailed component design, data flow diagrams |
| [folder structure](docs/folder_structure.md) | Everyone | This file | Directory organization and file purposes |

**Recommended Reading**:
1. Start with `user_guide.md` to get the pipeline running
2. Read `walkthrough.md` for detailed step-by-step instructions
3. Review `project_overview.md` to understand the "why"
4. Study `system_architecture.txt` for deep technical knowledge
5. Execute `test_cases.md` to validate your setup
6. Monitor using `performance_metrics.md` for baselines


### [Test Scripts](tests/)

**Purpose**: Automated testing infrastructure (currently placeholder, can be expanded).

**Potential Contents** (for future development):

```
tests/
├── test_data_generator.py
│   └── Unit tests for CSV generation
│
├── test_spark_job.py
│   └── Integration tests for Spark streaming
│
├── test_database.sql
│   └── Database validation queries
│
└── conftest.py
    └── Pytest configuration
```

**Current State**: Directory exists for future test expansion. Tests can be run manually via test_cases.md.

## File Sizes & Storage Plan

### Typical Sizes

| Component | Size | Notes |
|-----------|------|-------|
| Python scripts | ~30 KB | data_generator, spark job, reset utility |
| Documentation | ~150 KB | All .md + .txt files |
| JDBC driver | ~800 KB | postgresql-42.7.3.jar |
| Single CSV file | 5-50 KB | Depends on record count |
| 1 hour of data | ~500 MB | ~2000-3000 CSV files, input_data dir |
| Database table | ~500 MB (1M records) | Depends on storage backend |

### Storage Growth

```
Over time, accumulated size:

Day 1:  1 GB   (input_data: 100 MB, db: 900 MB)
Week 1: 10 GB  (input_data: 700 MB, db: 9.3 GB)
Month 1: 30 GB (input_data: 2 GB, db: 28 GB)
```

**Recommendations**:
- Archive old CSV files monthly (keep for replay ability)
- Use database retention policies (e.g., keep 90 days, archive rest)
- Monitor `data/input_data/` size; clear manually if needed


## Git Repository Structure (for Version Control)

**Recommended `.gitignore`**:

```
# Generated data (too large, regenerable)
data/input_data/**
data/checkpoint/**

# Logs
*.log
data/logs/

# IDE
.vscode/
.idea/
*.swp

# Python
__pycache__/
*.pyc
venv/
env/

# OS
.DS_Store
Thumbs.db

# Confidential
config/postgres_connection_details.txt  # IMPORTANT: Don't commit passwords!
```

**What TO commit**:
- All `.py` scripts
- All `.md` documentation
-  [`config/postgres_setup.sql`](config/postgres_setup.sql
-  [`requirements.txt`](requirements.txt)
-  [`.gitignore`](.gitignore)

**What NOT to commit**:
- ❌ `data/input_data/*.csv` (regenerable, large)
- ❌ `data/checkpoint/` (runtime state)
- ❌ `*.log` files
- ❌ `config/postgres_connection_details.txt` (contains password)

---

## Directory Permissions

**Recommended Unix Permissions**:

```bash
# Directories: rwxr-xr-x (755)
chmod 755 src/ data/ config/ lib/ docs/ tests/

# Python scripts: rwxr-xr-x (755)
chmod 755 src/*.py

# Config files: rw-r--r-- (644)
chmod 644 config/*.txt config/*.sql

# Data files: rw-r--r-- (644)
chmod 644 data/input_data/*.csv

# Sensitive: rw------- (600) - only owner can read
chmod 600 config/postgres_connection_details.txt
```

**Windows Equivalent**: Use NTFS security settings to restrict Authenticated Users to Read-only on sensitive files.

---

## Quick File Reference

**Need to...**  
→ **Start the pipeline?** See `src/data_generator.py` and `src/spark_streaming_to_postgres.py`

→ **Set up database?** Run `config/postgres_setup.sql`

→ **Update DB credentials?** Edit `config/postgres_connection_details.txt`

→ **Learn system design?** Read `docs/system_architecture.txt`

→ **Troubleshoot issues?** Check `docs/user_guide.md` (Troubleshooting section)

→ **Test everything?** Follow `docs/test_cases.md`

→ **Measure performance?** Review `docs/performance_metrics.md`

→ **First-time setup?** Follow `docs/walkthrough.md`

---

## Project Statistics

| Metric | Value |
|--------|-------|
| Total Python lines of code | ~900 LOC |
| Total documentation | ~1,500 lines |
| Number of source scripts | 3 |
| Number of test cases | 16 |
| Database tables | 1 |
| Database indexes | 4 |
| Configuration files | 2 |
| Documentation files | 7 |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 2026 | Initial release with complete architecture |

---

**Last Updated**: February 2026
**Author:** KWISANGA Ernest
