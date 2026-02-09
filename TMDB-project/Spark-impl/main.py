#!/usr/bin/env python3
"""
TMDB Movie Data Analysis - Main Orchestration Script

This script orchestrates the complete pipeline:
1. Fetch movie data from TMDB API
2. Clean and transform data using Spark
3. Generate KPI analysis report
4. Create visualizations
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from model.logger import get_logger
from model.config import RAW_DATA_PATH, PLOTS_DIR

logger = get_logger(__name__)


def print_banner(text: str):
    """Print a formatted banner."""
    width = 80
    print("\n" + "="*width)
    print(f"  {text.center(width-4)}")
    print("="*width + "\n")


def step_1_fetch_data():
    """Step 1: Fetch movie data from TMDB API."""
    print_banner("STEP 1: FETCHING MOVIE DATA FROM TMDB API")
    
    try:
        from model.ingestion.fetch_data import run_async_ingestion
        
        logger.info("Starting API data ingestion...")
        run_async_ingestion()
        logger.info("API data ingestion completed successfully!")
        
        # Verify data was fetched
        json_files = list(RAW_DATA_PATH.glob("*.json"))
        logger.info(f"Found {len(json_files)} batch files in raw data directory")
        
        if not json_files:
            logger.warning("No batch files found. This might indicate issues with the API.")
            return False
        return True
        
    except Exception as e:
        logger.error(f"Step 1 failed: {e}")
        return False


def step_2_etl_transformation():
    """Step 2: Clean and transform data using Spark."""
    print_banner("STEP 2: SPARK ETL TRANSFORMATION")
    
    try:
        from model.processing.etl import run_etl
        
        logger.info("Starting ETL transformation...")
        run_etl()
        logger.info("ETL transformation completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Step 2 failed: {e}")
        return False


def step_3_kpi_analysis():
    """Step 3: Generate KPI analysis report."""
    print_banner("STEP 3: GENERATING KPI ANALYSIS")
    
    try:
        from model.analytics.kpi import create_spark_session, generate_report
        
        logger.info("Starting KPI analysis...")
        spark = create_spark_session()
        generate_report(spark)
        spark.stop()
        logger.info("KPI analysis completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Step 3 failed: {e}")
        return False


def step_4_visualizations():
    """Step 4: Create visualizations."""
    print_banner("STEP 4: CREATING VISUALIZATIONS")
    
    try:
        from model.visualization.plots import create_all_visualizations
        from model.processing.etl import create_spark_session
        
        logger.info("Starting visualization generation...")
        
        # Load processed data
        data_path = str(Path(project_root) / "data" / "processed").replace("\\", "/")
        spark = create_spark_session()
        
        try:
            df_spark = spark.read.parquet(data_path)
            df_pandas = df_spark.toPandas()
            
            logger.info(f"Loaded {len(df_pandas)} records for visualization")
            
            # Create all visualizations
            create_all_visualizations(df_pandas, PLOTS_DIR)
            
            logger.info("Visualization generation completed successfully!")
            return True
        finally:
            spark.stop()
        
    except Exception as e:
        logger.error(f"Step 4 failed: {e}")
        return False


def step_5_summary():
    """Step 5: Display summary and next steps."""
    print_banner("SUMMARY & NEXT STEPS")
    
    from model.config import KPI_REPORT_PATH, PLOTS_DIR
    
    summary = f"""
📊 PROJECT COMPLETION SUMMARY
{'='*80}

✓ Data Pipeline Completed Successfully!

Generated Outputs:
  1. KPI Report: {KPI_REPORT_PATH}
  2. Plots Directory: {PLOTS_DIR}/
     - revenue_vs_budget.png
     - roi_by_genre.png
     - popularity_vs_rating.png
     - yearly_trends.png
     - franchise_vs_standalone.png
     - rating_distribution.png
     - top_directors.png
     - genre_performance.png

📁 Project Structure:
  - data/raw/          → Raw JSON files from API
  - data/processed/    → Cleaned Parquet files (partitioned by year)
  - output/kpi_analysis.txt → Detailed KPI report
  - output/plots/      → All visualizations

📖 Next Steps:
  1. Review the KPI report for insights
  2. Open visualizations in your preferred image viewer
  3. Open the Jupyter notebook for interactive analysis
  4. Consider the following analysis areas:
     ✓ Top performing movies and franchises
     ✓ Director success metrics
     ✓ Genre trends and patterns
     ✓ Revenue predictions for future projects

🎬 To explore interactively, open:
  → notebooks/analysis.ipynb

Questions? Check the logs in output/logs/ for detailed execution information.
"""
    print(summary)


def main():
    """Main orchestration function."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "TMDB MOVIE DATA ANALYSIS WITH SPARK".center(78) + "║")
    print("║" + "Complete Analytics Pipeline".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    start_time = time.time()
    
    # Track completion
    steps = [
        ("Fetching Data from API", step_1_fetch_data),
        ("ETL Transformation", step_2_etl_transformation),
        ("KPI Analysis", step_3_kpi_analysis),
        ("Visualization", step_4_visualizations),
    ]
    
    completed = []
    failed = []
    
    for step_name, step_func in steps:
        try:
            logger.info(f"\n{'='*80}")
            logger.info(f"Starting >>> {step_name}")
            logger.info(f"{'='*80}\n")
            
            if step_func():
                completed.append(step_name)
                logger.info(f"✓ {step_name} COMPLETED")
            else:
                failed.append(step_name)
                logger.error(f"✗ {step_name} FAILED")
                # Continue to next step instead of breaking
        except KeyboardInterrupt:
            logger.warning("Pipeline interrupted by user")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error in {step_name}: {e}")
            failed.append(step_name)
    
    # Print summary
    duration = time.time() - start_time
    
    print_banner(f"PIPELINE EXECUTION SUMMARY")
    
    if completed:
        print("✓ COMPLETED STEPS:")
        for step in completed:
            print(f"  ✓ {step}")
    
    if failed:
        print("\n✗ FAILED STEPS:")
        for step in failed:
            print(f"  ✗ {step}")
    
    print(f"\nTotal Execution Time: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"Completion Rate: {len(completed)}/{len(steps)} steps")
    print()
    
    # If all steps completed, show summary
    if not failed:
        step_5_summary()
        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY! 🎉\n")
        return 0
    else:
        print("\n⚠️  PIPELINE COMPLETED WITH ERRORS ⚠️\n")
        print("Please review the logs for more details:")
        print("  - output/logs/ingestion.log")
        print("  - output/logs/etl.log")
        print("  - output/logs/analytics.log")
        print("  - output/logs/project.log")
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
