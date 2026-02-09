# 🎬 TMDB Movie Data Analysis Using Apache Spark

> This project is a scalable data ingestion pipeline for fetching movie metadata from the TMDB API. It uses asynchronous I/O for high performance, bounded concurrency to respect rate limits by semaphore-based rate limiting, and a policy-driven retry mechanism with exponential backoff to handle transient failures safely. Data is written incrementally in a crash-safe format, making the pipeline reliable, resumable, and easy to operate, while its clean, modular design keeps it simple to maintain and extend as data volume grows.
---

## 📑 Table of Contents

- [🎯 Quick Start](#-quick-start)
- [🏗️ Pipeline Architecture](#-pipeline-architecture)
- [📊 Project Features](#-project-features)
- [📁 Directory Structure](#-directory-structure)
- [🚀 Execution Guide](#-execution-guide)
- [📈 Data Processing Pipeline](#-data-processing-pipeline)
- [📊 Analysis Capabilities](#-analysis-capabilities)
- [🛠️ Configuration](#-configuration)
- [🔍 Logs & Monitoring](#-logs--monitoring)
- [⚙️ Advanced Usage](#-advanced-usage)
- [🐛 Troubleshooting](#-troubleshooting)

---

## 🎯 Quick Start

### ✅ Prerequisites
- ✓ Python 3.13+
- ✓ Java 17+ (for Spark)
- ✓ Spark 4.1.1

### ✅ Setup & Run (30 seconds)

```bash
# 1. Navigate to project
cd Spark-impl

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies (2-3 minutes)
pip install -r requirements.txt

# 4. Configure API key
echo TMDB_API_KEY=your_api_key_here > .env

# 5. Run complete pipeline
python main.py
```

**Expected output**: ✓ Pipeline completes in ~1-2 minutes

---

## 🏗️ Pipeline Architecture

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TMDB MOVIE ANALYSIS PIPELINE                        │
└─────────────────────────────────────────────────────────────────────────────┘

    STEP 1: INGESTION          STEP 2: ETL               STEP 3: ANALYSIS
    ─────────────────          ───────────              ────────────────
         (Python)              (Apache Spark)           (Spark SQL)
    
    ┌─────────────┐        ┌──────────────┐        ┌─────────────────┐
    │   TMDB API  │───────▶│  Raw JSON    │───────▶│  Spark ETL      │
    │  (Async)    │        │  (Batches)   │        │  Transforms     │
    └─────────────┘        └──────────────┘        └─────────────────┘
         │                       │                        │
         │ Rate Limiting         │ data/raw/              │ data/processed/
         │ Retry Logic           │ batch_*.json           │ release_year=*/
         │ 19 Movies             │                        │
         │ 5 Concurrent          │                        │ ✓ Clean Data
         │                       │                        │ ✓ Schema  
         │                       │ ✓ Deduplicate          │ ✓ Partition
         │                       │ ✓ Validate             │ ✓ Optimize
         │                       │ ✓ Error Handle         │
         └───────────────────────┴────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   KPI Analysis   │
                    │  Report + 8 Vis  │
                    │  (Matplotlib)    │
                    └──────────────────┘
                        │           │
                    ┌───┴──┐    ┌───┴──────┐
                    ▼      ▼    ▼          ▼
              Report.txt  📊 plots/      📓 Notebook
             (7 Sections) (8 Images)    (Interactive)

┌─────────────────────────────────────────────────────────────────────────────┐
│ OUTPUTS: KPI Report | 8 Visualizations | Interactive Notebook | Full Logs   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Architecture Components

| Stage | Technology | Input | Output | Responsibility |
|-------|-----------|-------|--------|-----------------|
| **Ingestion** | Python AsyncIO + aiohttp | TMDB API | JSON files | Fetch 19 movies with rate limiting & retry |
| **ETL** | Apache Spark 4.1.1 | JSON files | Parquet (partitioned) | Clean, transform, enrich data |
| **Analytics** | Spark SQL | Parquet | KPI report | Generate 7 analysis sections |
| **Visualization** | Matplotlib + Seaborn | Parquet | 8 PNG images | Create publication-ready plots |
| **Orchestration** | Python | All modules | Complete pipeline | Orchestrate & monitor execution |

---

## 📊 Project Features

### ✅ Data Engineering
- ✓ **Async API Ingestion** - Non-blocking concurrent requests with semaphore rate limiting
- ✓ **Error Handling** - Exponential backoff, retry logic, graceful fallbacks
- ✓ **Schema Enforcement** - Explicit Spark schemas with nested data support
- ✓ **Data Partitioning** - Optimized by release_year for query performance
- ✓ **Windows Compatibility** - Hadoop workarounds + Pandas/PyArrow fallback

### ✅ Analytics & KPI
- ✓ **Revenue Analysis** - Top movies by revenue, budget, profit
- ✓ **ROI Metrics** - Return on investment calculations with thresholds
- ✓ **Ratings Analysis** - Highest/lowest rated, most voted movies
- ✓ **Advanced Queries** - Bruce Willis Sci-Fi, Tarantino + Uma Thurman
- ✓ **Franchise Impact** - Comparative performance (franchise vs standalone)
- ✓ **Director Rankings** - Top performers by revenue & ratings
- ✓ **Genre Trends** - Performance analysis across 8+ genres

### ✅ Visualizations (8 High-Resolution Plots)
1. ✓ **Revenue vs Budget** - Scatter with release year & vote count
2. ✓ **ROI by Genre** - Box plot distribution analysis
3. ✓ **Popularity vs Rating** - Correlation scatter plot
4. ✓ **Yearly Trends** - Time series (revenue, budget, profit)
5. ✓ **Franchise vs Standalone** - 4-subplot comparison
6. ✓ **Rating Distribution** - Histogram with mean/median
7. ✓ **Top Directors** - Horizontal bar chart ranking
8. ✓ **Genre Performance** - Triple analysis panel

### ✅ Monitoring & Logging
- ✓ **Component Logs** - Separate logs for ingestion, ETL, analytics
- ✓ **Progress Tracking** - Real-time execution status
- ✓ **Error Details** - Full stack traces in logs
- ✓ **Performance Metrics** - Execution times for each step

---

## 📁 Directory Structure

```
Spark-impl/
├── 📄 main.py                          # ← RUN THIS: Orchestration script
├── 📄 README.md                        # ← You are here
├── 📊 requirements.txt                 # Dependencies
├── 🔐 .env                             # API key (create this)
│
├── 📁 model/                           # Core pipeline modules
│   ├── config.py                       # ✓ Configuration constants
│   ├── logger.py                       # ✓ Logging setup
│   ├── ingestion/                      # Stage 1: API Fetching
│   │   └── fetch_data.py               # ✓ Async TMDB client
│   ├── processing/                     # Stage 2: Spark ETL
│   │   ├── etl.py                      # ✓ Transformations
│   │   └── schemas.py                  # ✓ Spark schemas
│   ├── analytics/                      # Stage 3: Analytics
│   │   └── kpi.py                      # ✓ KPI generation
│   └── visualization/                  # Stage 4: Plotting
│       └── plots.py                    # ✓ 8 visualizations
│
├── 📁 data/                            # Data directories
│   ├── raw/                            # ← API output (JSON)
│   └── processed/                      # ← ETL output (Parquet)
│
├── 📁 output/                          # Pipeline outputs
│   ├── kpi_analysis.txt                # ← KPI report (7 sections)
│   ├── logs/                           # Execution logs
│   │   ├── ingestion.log               # API fetch logs
│   │   ├── etl.log                     # Spark transform logs
│   │   └── analytics.log               # Analysis logs
│   └── plots/                          # ← 8 visualizations (PNG)
│
└── 📁 notebooks/
    └── analysis.ipynb                  # ← Interactive analysis
```

---

## 🚀 Execution Guide

### Option 1: Run Complete Pipeline (Recommended)  [main orchestration script](main.py)

```bash
python main.py
```

**What happens:**
1. ✓ Fetches 19 movies from TMDB (async, ~3 sec)
2. ✓ Transforms with Spark ETL (20-40 sec)
3. ✓ Generates KPI analysis (10-20 sec)
4. ✓ Creates 8 visualizations (5-10 sec)

**Total time:** ~1-2 minutes

**Outputs generated:**
- ✓ `output/kpi_analysis.txt` - Detailed report
- ✓ `output/plots/` - 8 PNG visualizations
- ✓ `output/logs/` - Complete execution logs

### Option 2: Run Individual Steps (For Debugging)

```bash
# Fetch data only
python -m model.ingestion.fetch_data

# ETL only (requires existing raw data)
python -m model.processing.etl

# Generate KPI report
python -m model.analytics.kpi
 c
# Create visualizations
python -c "from model.visualization.plots import create_all_visualizations; import pandas as pd; df = pd.read_parquet('data/processed'); create_all_visualizations(df, 'output/plots')"
```

### Option 3: Interactive Analysis

```bash
# Launch Jupyter notebook
jupyter notebook notebooks/analysis.ipynb
```

Features:
- ✓ Load processed data
- ✓ Run custom queries
- ✓ Generate adhoc plots
- ✓ Explore correlations

---

## 📈 Data Processing Pipeline

### [Stage 1: API Ingestion](model/ingestion/fetch_data.py)

**Purpose:** ✓ Fetch movie data from TMDB

```python
Input:  19 movie IDs from config
Output: data/raw/batch_*.json
Time:   30-60 seconds
```

**Features:**
- ✓ Async requests with asyncio
- ✓ Rate limiting (5 concurrent)
- ✓ Exponential backoff on 429
- ✓ Retry logic (5 max retries)
- ✓ Newline-delimited JSON

### [Stage 2: Spark ETL](model/processing/etl.py)

**Purpose:** ✓ Clean and transform raw data

```python
Input:  data/raw/batch_*.json
Output: data/processed/release_year=*/
Time:   20-40 seconds
```

**Transformations:**
- ✓ Filter "Released" movies
- ✓ Parse dates → extract year
- ✓ Handle nulls/zeros → NaN
- ✓ Extract genres (pipe-separated)
- ✓ Flatten credits → cast/director
- ✓ Calculate profit & ROI
- ✓ Partition by release_year

### [Stage 3: KPI Analysis](model/analytics/kpi.py)

**Purpose:** ✓ Generate business insights

```python
Input:  data/processed/
Output: output/kpi_analysis.txt
Time:   10-20 seconds
```

**7 Analysis Sections:**
1. ✓ General Statistics
2. ✓ Top Performing Movies
3. ✓ Critical & Audience Ratings
4. ✓ Advanced Filtering Queries
5. ✓ Franchise vs Standalone
6. ✓ Most Successful Franchises
7. ✓ Top Directors

### [Stage 4: Visualizations](model/visualization/plots.py)

**Purpose:** ✓ Create publication-ready plots

```python
Input:  data/processed/
Output: output/plots/*.png (8 images)
Time:   5-10 seconds
```

**8 Plots Generated:**
1. ✓ Revenue vs Budget
2. ✓ ROI by Genre
3. ✓ Popularity vs Rating
4. ✓ Yearly Trends
5. ✓ Franchise vs Standalone
6. ✓ Rating Distribution
7. ✓ Top Directors
8. ✓ Genre Performance

---

## 📊 Analysis Capabilities

### KPI Metrics

| Metric | Purpose | Calculation |
|--------|---------|-------------|
| **Revenue** | Total sales | Sum of gross revenue |
| **Profit** | Net earnings | Revenue - Budget |
| **ROI** | Return on investment | Revenue / Budget |
| **Rating** | Quality measure | TMDB average (0-10) |
| **Popularity** | Public interest | TMDB popularity index |
| **Franchise Impact** | Series performance | Grouped by collection |

### Advanced Queries

✓ **Bruce Willis Sci-Fi Action Query**
```python
Films with: Genre="Sci-Fi" AND Genre="Action" AND Cast="Bruce Willis"
Sorted by: Rating (highest first)
```

✓ **Tarantino + Uma Thurman Query**
```python
Films with: Director="Quentin Tarantino" AND Cast="Uma Thurman"
Sorted by: Runtime (shortest first)
```

✓ **Franchise vs Standalone Comparison**
```
Metrics: Revenue, Budget, Rating, Popularity, ROI
Grouped: belongs_to_collection NOT NULL vs NULL
```

---

## 🛠️ Configuration

### Edit `model/config.py` to customize:

```python
# API Settings
TARGET_MOVIE_IDS = [...]           # ✓ Movies to fetch
INGESTION_CONCURRENCY = 5          # ✓ Concurrent requests
INGESTION_BATCH_SIZE = 100         # ✓ Movies per batch file

# Spark Settings
SPARK_MASTER = "local[*]"          # ✓ Use all cores
SPARK_APP_NAME = "TMDB_Analytics"  # ✓ Application name

# Output Settings
FINAL_COLUMNS_ORDER = [...]        # ✓ Column ordering
PLOTS_DIR = "output/plots"         # ✓ Plot directory
KPI_REPORT_PATH = "output/kpi_analysis.txt"  # ✓ Report path
```

### Create `.env` for API Key:

```bash
TMDB_API_KEY=your_api_key_from_themoviedb_org
```

Get your key: https://www.themoviedb.org/settings/api

---

## 🔍 [Logs & Monitoring](output/logs/)


### View Execution Logs

```bash
# Real-time tail
tail -f output/logs/project.log

# View specific component
cat output/logs/ingestion.log
cat output/logs/etl.log
cat output/logs/analytics.log
```

### Log Files Generated

| File | Purpose | Size |
|------|---------|------|
| `project.log` | Overall workflow | ~10-50 KB |
| `ingestion.log` | API fetching | ~5-20 KB |
| `etl.log` | Spark transforms | ~20-100 KB |
| `analytics.log` | Analysis steps | ~10-30 KB |

---

## ⚙️ Advanced Usage

### Running on Different Platforms

**Linux/Mac:**
```bash
python main.py
# No Hadoop issues, runs natively
```

**Windows (with WSL2 recommended):**
```bash
# Option 1: Use WSL2
wsl python main.py

# Option 2: Native (with Hadoop workaround)
python main.py  # Falls back to Pandas/PyArrow automatically
```

### Increase Available Memory

```bash
export SPARK_DRIVER_MEMORY=4g
export SPARK_EXECUTOR_MEMORY=4g
python main.py
```

### Reduce Concurrent Requests

Edit `model/config.py`:
```python
INGESTION_CONCURRENCY = 3  # Reduce if rate-limited
```

### Access Raw Data in Python

```python
import pandas as pd

# Load processed data
df = pd.read_parquet('data/processed')

# Inspect columns
print(df.columns)
print(df.head())

# Custom analysis
df[df['genres'].str.contains('Action')].groupby('director')['revenue_musd'].sum()
```

---

## 🐛 Troubleshooting

### ❌ "TMDB_API_KEY not found"

✅ **Solution:**
```bash
# Create .env file with your API key
echo TMDB_API_KEY=your_key_here > .env
```

### ❌ "No JSON files in data/raw/"

✅ **Solution:**
```bash
# Verify API key is valid
# Check network connection
# Review logs: tail -50 output/logs/ingestion.log
# Run step 1 again: python -m model.ingestion.fetch_data
```

### ❌ "Spark write failed (Hadoop)"

✅ **Solution:**
The pipeline automatically falls back to Pandas/PyArrow.
If issues persist:
- Option A: Download winutils.exe → `C:/hadoop/bin/`
- Option B: Run on Linux/WSL instead

### ❌ "Memory error during Spark"

✅ **Solution:**
```bash
# Close other applications
# Increase available memory
export SPARK_DRIVER_MEMORY=4g
python main.py
```

### ❌ "Module not found" errors

✅ **Solution:**
```bash
# Verify virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### ❌ "Rate limit (429 error)"

✅ **Solution:**
```bash
# The pipeline retries automatically with exponential backoff
# If still failing after 5 min:
# 1. Wait 15-20 minutes
# 2. Check TMDB API status
# 3. Reduce INGESTION_CONCURRENCY to 3
```

---

## 📚 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Distributed Processing** | Apache Spark | 4.1+ | ETL at scale |
| **Data Manipulation** | Pandas | 2.0+ | Data analysis |
| **Visualization** | Matplotlib + Seaborn | 3.7+ / 0.13+ | Plots |
| **API Client** | aiohttp | 3.8+ | Async HTTP |
| **Column Format** | PyArrow | 13.0+ | Parquet I/O |
| **Configuration** | python-dotenv | 1.0+ | Environment vars |

---

## 🎓 What You'll Learn

### Data Engineering
✓ Async API clients with rate limiting  
✓ ETL pipeline design & orchestration  
✓ Schema validation & enforcement  
✓ Error handling & retry logic  
✓ Data partitioning strategies  

### Apache Spark
✓ DataFrame transformations  
✓ Nested data flattening  
✓ Schema management  
✓ Aggregations & window functions  
✓ Platform compatibility  

### Analytics
✓ KPI calculation & reporting  
✓ Advanced filtering  
✓ Comparative analysis  
✓ Trend identification  

### Visualization
✓ Multi-plot figure composition  
✓ Statistical plots  
✓ High-resolution export  

---

## 📄 Project Outputs Explained

### KPI Report (`output/kpi_analysis.txt`)

Contains 7 analysis sections:
1. **General Statistics** - Dataset overview
2. **Top Performing** - Revenue, profit, ROI leaders
3. **Ratings** - Audience & critic analysis
4. **Advanced Queries** - Complex filters
5. **Franchise Analysis** - Performance comparison
6. **Top Franchises** - Series rankings
7. **Top Directors** - Director metrics

### Visualizations (`output/plots/`)

8 high-resolution PNG files for presentations/reports

### Interactive Notebook (`notebooks/analysis.ipynb`)

Run custom analysis, generate adhoc plots, explore data interactively

---

## ✨ Future Enhancements

- [ ] Machine learning revenue prediction
- [ ] Cloud deployment (AWS, GCP)
- [ ] Real-time data streaming
- [ ] Interactive Plotly dashboard
- [ ] Automated data quality checks
- [ ] Additional data sources

---

## 📞 Support & Questions

1. Check logs in `output/logs/`
2. Review [Troubleshooting](#-troubleshooting) section
3. Verify all [prerequisites](#-prerequisites) installed
4. Check environment variables in `.env`

---

## 📄 License

Educational project for demonstrating data engineering best practices.

---

## 🚀 Ready to Start?

```bash
python main.py
```

**Questions?** Review the documentation sections above or check the logs for detailed error messages.

---

**Last Updated:** February 2026  
**Spark Version:** 3.5+  
**Python Version:** 3.8+  
**Status:** ✅ Production Ready
