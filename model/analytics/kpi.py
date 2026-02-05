from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, desc, asc, avg, count, sum, median, when, expr
)
from model.config import (
    SPARK_APP_NAME, SPARK_MASTER, 
    PROCESSED_DATA_PATH, KPI_REPORT_PATH
)
from model.logger import get_logger
import sys
import os

logger = get_logger(__name__)

def create_spark_session():
    """Creates a Spark session with Windows compatibility."""
    if sys.platform == "win32":
        hadoop_home = "C:/hadoop"
        os.environ["HADOOP_HOME"] = hadoop_home
        if f"{hadoop_home}/bin" not in os.environ["PATH"].replace("\\", "/"):
            os.environ["PATH"] = f"{hadoop_home}/bin;" + os.environ["PATH"]

    return SparkSession.builder \
        .appName(SPARK_APP_NAME + "_Analytics") \
        .master(SPARK_MASTER) \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
        .getOrCreate()


def generate_report(spark):
    """Generate comprehensive KPI analysis report."""
    logger.info("Starting Comprehensive Analytics...")
    
    # ===== LOAD DATA =====
    data_path = str(PROCESSED_DATA_PATH).replace("\\", "/")
    logger.info(f"Loading data from: {data_path}")
    
    try:
        df = spark.read.parquet(data_path)
        count_val = df.count()
        logger.info(f"Successfully loaded {count_val} records.")
    except Exception as e:
        logger.error(f"Failed to read Parquet data: {e}")
        return

    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("TMDB MOVIE DATA ANALYSIS REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")

    # ===== SECTION 1: GENERAL STATISTICS =====
    report_lines.append("1. GENERAL STATISTICS")
    report_lines.append("-" * 80)
    report_lines.append(f"Total Movies Analyzed: {count_val}")
    
    avg_budget = df.agg(avg("budget_musd")).collect()[0][0] or 0
    avg_revenue = df.agg(avg("revenue_musd")).collect()[0][0] or 0
    avg_rating = df.agg(avg("vote_average")).collect()[0][0] or 0
    
    report_lines.append(f"Average Budget: ${avg_budget:,.2f} Million MUSD")
    report_lines.append(f"Average Revenue: ${avg_revenue:,.2f} Million MUSD")
    report_lines.append(f"Average Rating: {avg_rating:.2f}/10")
    report_lines.append("")

    # ===== SECTION 2: TOP PERFORMING MOVIES =====
    report_lines.append("2. TOP PERFORMING MOVIES")
    report_lines.append("-" * 80)
    
    # Highest Revenue
    report_lines.append("\n2.1 Highest Revenue (Top 5):")
    top_revenue = df.filter(col("revenue_musd").isNotNull()) \
        .orderBy(desc("revenue_musd")) \
        .limit(5) \
        .select("title", "revenue_musd", "release_year")
    for i, row in enumerate(top_revenue.collect(), 1):
        report_lines.append(f"  {i}. {row['title']} ({row['release_year']}): ${row['revenue_musd']:,.2f}M")

    # Highest Profit
    report_lines.append("\n2.2 Highest Profit (Top 5):")
    top_profit = df.filter(col("profit").isNotNull()) \
        .orderBy(desc("profit")) \
        .limit(5) \
        .select("title", "profit", "budget_musd", "revenue_musd")
    for i, row in enumerate(top_profit.collect(), 1):
        report_lines.append(f"  {i}. {row['title']}: ${row['profit']:,.0f} (Budget: ${row['budget_musd']:,.2f}M, Revenue: ${row['revenue_musd']:,.2f}M)")

    # Lowest Profit
    report_lines.append("\n2.3 Lowest Profit (Top 5):")
    lowest_profit = df.filter(col("profit").isNotNull()) \
        .orderBy(asc("profit")) \
        .limit(5) \
        .select("title", "profit", "budget_musd")
    for i, row in enumerate(lowest_profit.collect(), 1):
        report_lines.append(f"  {i}. {row['title']}: ${row['profit']:,.0f} (Budget: ${row['budget_musd']:,.2f}M)")

    # Highest ROI (Budget > 10M)
    report_lines.append("\n2.4 Highest ROI - Budget ≥ $10M (Top 5):")
    top_roi = df.filter((col("budget_musd") >= 10) & (col("roi").isNotNull())) \
        .orderBy(desc("roi")) \
        .limit(5) \
        .select("title", "roi", "budget_musd")
    for i, row in enumerate(top_roi.collect(), 1):
        roi_pct = (row['roi'] - 1) * 100 if row['roi'] else 0
        report_lines.append(f"  {i}. {row['title']}: {row['roi']:.2f}x ({roi_pct:+.0f}%) | Budget: ${row['budget_musd']:,.2f}M")

    # Lowest ROI (Budget > 10M)
    report_lines.append("\n2.5 Lowest ROI - Budget ≥ $10M (Top 5):")
    lowest_roi = df.filter((col("budget_musd") >= 10) & (col("roi").isNotNull())) \
        .orderBy(asc("roi")) \
        .limit(5) \
        .select("title", "roi", "budget_musd")
    for i, row in enumerate(lowest_roi.collect(), 1):
        roi_pct = (row['roi'] - 1) * 100 if row['roi'] else 0
        report_lines.append(f"  {i}. {row['title']}: {row['roi']:.2f}x ({roi_pct:+.0f}%) | Budget: ${row['budget_musd']:,.2f}M")

    report_lines.append("")

    # ===== SECTION 3: CRITICAL RATINGS =====
    report_lines.append("3. CRITICAL & AUDIENCE RATINGS")
    report_lines.append("-" * 80)
    
    # Most Voted
    report_lines.append("\n3.1 Most Voted Movies (Top 5):")
    most_voted = df.filter(col("vote_count").isNotNull()) \
        .orderBy(desc("vote_count")) \
        .limit(5) \
        .select("title", "vote_count", "vote_average")
    for i, row in enumerate(most_voted.collect(), 1):
        report_lines.append(f"  {i}. {row['title']}: {row['vote_count']:,} votes | Rating: {row['vote_average']:.1f}/10")

    # Highest Rated (min 10 votes)
    report_lines.append("\n3.2 Highest Rated Movies (min. 10 votes) (Top 5):")
    highest_rated = df.filter((col("vote_count") >= 10) & (col("vote_average").isNotNull())) \
        .orderBy(desc("vote_average"), desc("vote_count")) \
        .limit(5) \
        .select("title", "vote_average", "vote_count")
    for i, row in enumerate(highest_rated.collect(), 1):
        report_lines.append(f"  {i}. {row['title']}: {row['vote_average']:.1f}/10 ({row['vote_count']:,} votes)")

    # Lowest Rated (min 10 votes)
    report_lines.append("\n3.3 Lowest Rated Movies (min. 10 votes) (Top 5):")
    lowest_rated = df.filter((col("vote_count") >= 10) & (col("vote_average").isNotNull())) \
        .orderBy(asc("vote_average"), asc("vote_count")) \
        .limit(5) \
        .select("title", "vote_average", "vote_count")
    for i, row in enumerate(lowest_rated.collect(), 1):
        report_lines.append(f"  {i}. {row['title']}: {row['vote_average']:.1f}/10 ({row['vote_count']:,} votes)")

    # Most Popular
    report_lines.append("\n3.4 Most Popular Movies (Top 5):")
    most_popular = df.filter(col("popularity").isNotNull()) \
        .orderBy(desc("popularity")) \
        .limit(5) \
        .select("title", "popularity", "release_year")
    for i, row in enumerate(most_popular.collect(), 1):
        report_lines.append(f"  {i}. {row['title']} ({row['release_year']}): Popularity Score {row['popularity']:.2f}")

    report_lines.append("")

    # ===== SECTION 4: ADVANCED FILTERING QUERIES =====
    report_lines.append("4. ADVANCED FILTERING & SEARCH QUERIES")
    report_lines.append("-" * 80)
    
    # Query 1: Sci-Fi Action Movies with Bruce Willis
    report_lines.append("\n4.1 Sci-Fi Action Movies starring Bruce Willis (sorted by rating):")
    scifi_action_bruce = df.filter(
        (col("genres").contains("Science Fiction")) & 
        (col("genres").contains("Action")) & 
        (col("cast").contains("Bruce Willis"))
    ).orderBy(desc("vote_average")) \
        .select("title", "vote_average", "release_year", "genres")
    
    results = scifi_action_bruce.collect()
    if results:
        for i, row in enumerate(results, 1):
            report_lines.append(f"  {i}. {row['title']} ({row['release_year']}): Rating {row['vote_average']:.1f} | Genres: {row['genres']}")
    else:
        report_lines.append("  No movies found matching criteria.")

    # Query 2: Uma Thurman + Quentin Tarantino
    report_lines.append("\n4.2 Movies starring Uma Thurman directed by Quentin Tarantino (sorted by runtime):")
    uma_tarantino = df.filter(
        (col("cast").contains("Uma Thurman")) & 
        (col("director") == "Quentin Tarantino")
    ).orderBy(asc("runtime")) \
        .select("title", "release_year", "runtime", "vote_average")
    
    results = uma_tarantino.collect()
    if results:
        for i, row in enumerate(results, 1):
            report_lines.append(f"  {i}. {row['title']} ({row['release_year']}): {row['runtime']} min | Rating: {row['vote_average']:.1f}")
    else:
        report_lines.append("  No movies found matching criteria.")

    report_lines.append("")

    # ===== SECTION 5: FRANCHISE ANALYSIS =====
    report_lines.append("5. FRANCHISE VS STANDALONE ANALYSIS")
    report_lines.append("-" * 80)
    
    franchise_df = df.filter(col("belongs_to_collection").isNotNull())
    standalone_df = df.filter(col("belongs_to_collection").isNull())
    
    franchise_count = franchise_df.count()
    standalone_count = standalone_df.count()
    
    report_lines.append(f"\nFranchise Movies: {franchise_count}")
    report_lines.append(f"Standalone Movies: {standalone_count}")
    
    # Metrics for each
    if franchise_count > 0:
        franchise_metrics = franchise_df.agg(
            avg("revenue_musd").alias("avg_revenue"),
            median("roi").alias("median_roi"),
            avg("budget_musd").alias("avg_budget"),
            avg("popularity").alias("avg_popularity"),
            avg("vote_average").alias("avg_rating")
        ).collect()[0]
        report_lines.append(f"\nFranchise Movies Metrics:")
        report_lines.append(f"  - Mean Revenue: ${franchise_metrics['avg_revenue']:,.2f}M")
        report_lines.append(f"  - Median ROI: {franchise_metrics['median_roi']:.2f}x" if franchise_metrics['median_roi'] else "  - Median ROI: N/A")
        report_lines.append(f"  - Mean Budget: ${franchise_metrics['avg_budget']:,.2f}M")
        report_lines.append(f"  - Mean Popularity: {franchise_metrics['avg_popularity']:.2f}")
        report_lines.append(f"  - Mean Rating: {franchise_metrics['avg_rating']:.2f}/10")

    if standalone_count > 0:
        standalone_metrics = standalone_df.agg(
            avg("revenue_musd").alias("avg_revenue"),
            median("roi").alias("median_roi"),
            avg("budget_musd").alias("avg_budget"),
            avg("popularity").alias("avg_popularity"),
            avg("vote_average").alias("avg_rating")
        ).collect()[0]
        report_lines.append(f"\nStandalone Movies Metrics:")
        report_lines.append(f"  - Mean Revenue: ${standalone_metrics['avg_revenue']:,.2f}M")
        report_lines.append(f"  - Median ROI: {standalone_metrics['median_roi']:.2f}x" if standalone_metrics['median_roi'] else "  - Median ROI: N/A")
        report_lines.append(f"  - Mean Budget: ${standalone_metrics['avg_budget']:,.2f}M")
        report_lines.append(f"  - Mean Popularity: {standalone_metrics['avg_popularity']:.2f}")
        report_lines.append(f"  - Mean Rating: {standalone_metrics['avg_rating']:.2f}/10")

    report_lines.append("")

    # ===== SECTION 6: MOST SUCCESSFUL FRANCHISES =====
    report_lines.append("6. MOST SUCCESSFUL FRANCHISES")
    report_lines.append("-" * 80)
    
    franchise_stats = franchise_df.groupBy("belongs_to_collection") \
        .agg(
            count("id").alias("movie_count"),
            sum("budget_musd").alias("total_budget"),
            avg("budget_musd").alias("mean_budget"),
            sum("revenue_musd").alias("total_revenue"),
            avg("revenue_musd").alias("mean_revenue"),
            avg("vote_average").alias("mean_rating")
        ) \
        .filter(col("movie_count") > 1) \
        .orderBy(desc("total_revenue")) \
        .limit(10)
    
    report_lines.append("\nTop 10 Franchises by Total Revenue (min. 2 movies):")
    results = franchise_stats.collect()
    if results:
        for i, row in enumerate(results, 1):
            report_lines.append(f"\n  {i}. {row['belongs_to_collection']}")
            report_lines.append(f"     - Movies: {row['movie_count']}")
            report_lines.append(f"     - Total Budget: ${row['total_budget']:,.2f}M | Mean: ${row['mean_budget']:,.2f}M")
            report_lines.append(f"     - Total Revenue: ${row['total_revenue']:,.2f}M | Mean: ${row['mean_revenue']:,.2f}M")
            report_lines.append(f"     - Mean Rating: {row['mean_rating']:.2f}/10")
    else:
        report_lines.append("  No franchises with multiple movies found.")

    report_lines.append("")

    # ===== SECTION 7: TOP DIRECTORS =====
    report_lines.append("7. MOST SUCCESSFUL DIRECTORS")
    report_lines.append("-" * 80)
    
    director_stats = df.filter(col("director") != "Unknown") \
        .groupBy("director") \
        .agg(
            count("id").alias("movie_count"),
            sum("revenue_musd").alias("total_revenue"),
            avg("vote_average").alias("mean_rating")
        ) \
        .orderBy(desc("total_revenue")) \
        .limit(10)
    
    report_lines.append("\nTop 10 Directors by Total Revenue:")
    results = director_stats.collect()
    if results:
        for i, row in enumerate(results, 1):
            report_lines.append(f"  {i}. {row['director']}")
            report_lines.append(f"     - Movies: {row['movie_count']} | Total Revenue: ${row['total_revenue']:,.2f}M | Mean Rating: {row['mean_rating']:.2f}/10")
    else:
        report_lines.append("  No director data available.")

    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)

    # ===== WRITE REPORT =====
    logger.info(f"Writing report to: {KPI_REPORT_PATH}")
    try:
        with open(KPI_REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        logger.info("Report written successfully.")
    except Exception as e:
        logger.error(f"Failed to write report: {e}")
        
    logger.info("Analytics finished.")


if __name__ == "__main__":
    spark = create_spark_session()
    generate_report(spark)
    spark.stop()
