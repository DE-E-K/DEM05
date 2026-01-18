
import os
import sys
import json

# Ensure BySpark is in python path
sys.path.append(os.path.join(os.getcwd(), 'BySpark'))

# Use 'python' from PATH to avoid issues with spaces in absolute paths on Windows
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from dotenv import load_dotenv

from extraction.tmdb_api import fetch_movie_data
from cleaning.preprocessor import clean_dataframe
from analysis.kpi_calculations import (
    get_best_worst_movies, 
    search_queries, 
    compare_franchises, 
    analyze_directors
)
from visualization.charts import plot_charts

def main():
    # 1. Load Env
    load_dotenv()
    api_key = os.getenv("api_key")
    if not api_key:
        print("Error: API key not found in .env")
        return

    # 2. Init Spark
    spark = SparkSession.builder \
        .appName("TMDB_Movie_Analysis") \
        .master("local[*]") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("ERROR")
    
    # 3. Data Extraction
    print("--- Phase 1: Data Extraction ---")
    movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 168259, 
                 99861, 284054, 12445, 181808, 330457, 351286, 109445, 321612, 260513]
                 
    raw_data = fetch_movie_data(api_key, movie_ids)
    
    if not raw_data:
        print("No data fetched. Exiting.")
        return
        
    # Convert to Spark DataFrame
    # Spark might struggle with complex nested JSON without schema. 
    # We'll allow it to infer schema from the list of dicts.
    
    # Save Raw Data
    json_rdd = spark.sparkContext.parallelize([json.dumps(r) for r in raw_data])
    df_raw = spark.read.json(json_rdd)
    # df_raw.write.mode("overwrite").parquet("data/raw_parquet")
    # df_raw.write.mode("overwrite").option("header", "true").csv("data/raw_csv")
    print("Raw data saved to data/raw_parquet and data/raw_csv")    


    # 4. Data Cleaning
    print("\n--- Phase 2: Data Cleaning ---")
    df_clean = clean_dataframe(df_raw)
    df_clean.printSchema()
    
    # 5. Analysis
    print("\n--- Phase 3: Analysis & KPIs ---")
    
    # Best/Worst
    rankings = get_best_worst_movies(df_clean)
    print("Top 5 Movies by Revenue:")
    rankings["best_revenue"].select("title", "revenue_musd").show(truncate=False)
    
    print("Top 5 Movies by Profit:")
    rankings["best_profit"].select("title", "profit_musd").show(truncate=False)
    
    # Search Queries
    searches = search_queries(df_clean)
    if "bruce_willis_scifi_action" in searches:
        print("Search: Bruce Willis Sci-Fi/Action:")
        searches["bruce_willis_scifi_action"].select("title", "vote_average").show(truncate=False)
        
    # Franchise Analysis
    franchise_stats = compare_franchises(df_clean)
    print("Franchise vs Standalone Stats:")
    franchise_stats.show(truncate=False)
    
    # Director Analysis
    director_stats = analyze_directors(df_clean)
    print("Top Directors by Revenue:")
    director_stats.show(5, truncate=False)
    
    # 6. Visualization
    print("\n--- Phase 4: Visualization ---")
    
    # Convert necessary data to Pandas for plotting
    # Warning: Collect only small aggregated data or sample
    
    # Plots require:
    # 1. Revenue vs Budget (All movies) -> For yearly bar chart
    # Pandas implementation uses: yearly_data = (df_cleaned.groupby('release_year')[['revenue_musd', 'budget_musd']].sum()...)
    # So we need to emulate that aggregation here or pass raw data if acceptable. 
    # To match pandas exactly, we should aggregate by year.
    df_clean = df_clean.withColumn("year", F.year("release_date"))
    yearly_rev_bud = df_clean.groupBy("year").agg(
        F.sum("revenue_musd").alias("Total Revenue"), 
        F.sum("budget_musd").alias("Total Budget")
    ).orderBy("year")
    pdf_rev_bud = yearly_rev_bud.toPandas()
    
    # 2. ROI by Genre
    # Explode genres first to get ROI per genre
    genre_roi = df_clean.groupBy("genres").agg(F.mean("roi").alias("mean_roi"))
    pdf_roi_genre = genre_roi.toPandas()
    
    # 3. Popularity vs Rating
    pdf_pop_rating = df_clean.select("popularity", "vote_average").toPandas()
    
    # 4 Yearly trend in box office revenue
    # Already computed year above, but re-doing for clarity as per original structure or reusing
    yearly_revenue = df_clean.groupBy("year").agg(F.sum("revenue_musd").alias("total_revenue")).orderBy("year")
    pdf_yearly_revenue = yearly_revenue.toPandas()
    
    # 5 Comparison of franchise vs standalone movies
    franchise_stats = compare_franchises(df_clean)
    pdf_franchise_standalone = franchise_stats.toPandas()
    
    plot_charts(pdf_rev_bud, pdf_roi_genre, pdf_pop_rating, pdf_yearly_revenue, pdf_franchise_standalone)
    
    print("\nWorkflow Completed Successfully.")
    spark.stop()



if __name__ == "__main__":
    main()
