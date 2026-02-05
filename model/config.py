import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base Project Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw"
PROCESSED_DATA_PATH = DATA_DIR / "processed"

# Output Directories
OUTPUT_DIR = BASE_DIR / "output"
PLOTS_DIR = OUTPUT_DIR / "plots"
KPI_REPORT_PATH = OUTPUT_DIR / "kpi_analysis.txt"

# Ensure directories exist
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# TMDB Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Spark Configuration
SPARK_APP_NAME = "TMDB_Analytics"
SPARK_MASTER = "local[*]"  # Run locally with all cores

# Target Movie IDs for Ingestion (from requirements)
TARGET_MOVIE_IDS = [
    0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 
    24428, 168259, 99861, 284054, 12445, 181808, 330457, 
    351286, 109445, 321612, 260513
]

# Ingestion Configuration
INGESTION_CONCURRENCY = 5  # Number of concurrent requests
INGESTION_BATCH_SIZE = 100 # Movies per output file

# ETL Configuration
COLUMNS_TO_DROP = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
FINAL_COLUMNS_ORDER = [
    'id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection', 
    'original_language', 'budget_musd', 'revenue_musd', 'production_companies', 
    'production_countries', 'vote_count', 'vote_average', 'popularity', 
    'runtime', 'overview', 'spoken_languages', 'poster_path', 'cast', 
    'cast_size', 'director', 'crew_size', 'profit', 'roi'
]

