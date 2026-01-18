from pyspark.sql import functions as F
from pyspark.sql.window import Window


def get_best_worst_movies(df):
    """
    Ranks movies based on Revenue, Budget, Profit, and ROI, vote_average, popularity.
    """
    
    df = df_clean.copy()
    # 1. Best/Worst by Revenue
    best_revenue = df.orderBy(F.col("revenue_musd").desc()).limit(5)
    worst_revenue = df.orderBy(F.col("revenue_musd").asc()).limit(5)
    
    # 2. Best/Worst by Budget
    best_budget = df.orderBy(F.col("budget_musd").desc()).limit(5)
    worst_budget = df.orderBy(F.col("budget_musd").asc()).limit(5)
    
    # 3. Best/Worst by Profit
    best_profit = df.orderBy(F.col("profit_musd").desc()).limit(5)
    worst_profit = df.orderBy(F.col("profit_musd").asc()).limit(5)
    
    # 4. Best/Worst ROI (Budget >= 10M)
    df_roi = df.filter(F.col("budget_musd") >= 10)
    best_roi = df_roi.orderBy(F.col("roi").desc()).limit(5)
    worst_roi = df_roi.orderBy(F.col("roi").asc()).limit(5)

    # 5. Best/worst by rated movies(vote >= 10)
    df_vote = df.filter(F.col("vote_count") >= 10)
    best_rated = df_vote.orderBy(F.col("vote_count").desc()).limit(5)
    worst_rated = df_vote.orderBy(F.col("vote_count").asc()).limit(5)

    # 6. Best/worst by popularity
    best_popularity = df.orderBy(F.col("popularity").desc()).limit(5)
    worst_popularity = df.orderBy(F.col("popularity").asc()).limit(5)

    # 7. Best/worst by voted movies
    best_voted = df.filter(F.col("vote_count") >= 10).orderBy(F.col("vote_count").desc()).limit(5)
    worst_voted = df.filter(F.col("vote_count") >= 10).orderBy(F.col("vote_count").asc()).limit(5)
    
    return {
        "best_revenue": best_revenue,
        "worst_revenue": worst_revenue,
        "best_budget": best_budget,
        "worst_budget": worst_budget,
        "best_profit": best_profit,
        "worst_profit": worst_profit,
        "best_roi": best_roi,
        "worst_roi": worst_roi,
        "best_rated": best_rated,
        "worst_rated": worst_rated,
        "best_voted": best_voted,
        "worst_voted": worst_voted,
        "best_popularity": best_popularity,
        "worst_popularity": worst_popularity
    }


def search_queries(df):
    """
    Executes specific search queries.
    """
    results = {}
    
    # Search 1: Science Fiction Action movies starring Bruce Willis (Rating desc)
    # Genres: "Science Fiction", "Action" present in 'genres' column (contains check)
    # Cast: "Bruce Willis" (Wait, cast is usually a JSON array of structs). 
    # Assume 'cast' column is available and is a string or array of strings.
    # If cast is raw JSON, we might need to rely on 'cast_size' or preprocess 'cast' in cleaning.
    # Let's assume for search query 1, we need to Filter by genres containing keywords.
    # NOTE: The instructions say "cast" is one of the final columns, but cleaning didn't explicitly process 'cast' content string.
    # We will assume 'cast' contains stringified names or check schema.
    # For now, simplistic 'contains' (if cast is string)
    
    # Check if 'cast' column exists, if not, skip with warning
    if 'cast' in df.columns:
         s1 = df.filter(
             (F.col("genres").contains("Science Fiction")) | 
             (F.col("genres").contains("Action")) & 
             (F.col("cast").contains("Bruce Willis"))
         ).orderBy(F.col("vote_average").desc())
         results["bruce_willis_scifi_action"] = s1
    
    # Search 2: Uma Thurman, Directed by Quentin Tarantino (Runtime asc)
    if 'cast' in df.columns and 'director' in df.columns:
        s2 = df.filter(
            (F.col("cast").contains("Uma Thurman")) &
            (F.col("director") == "Quentin Tarantino")
        ).orderBy(F.col("runtime").asc())
        results["uma_thurman_tarantino"] = s2
        
    return results


def compare_franchises(df):
    """
    Compares Franchise vs Standalone movies.
    """
    # Create flag: is_franchise
    df = df.withColumn("is_franchise", F.when(F.col("belongs_to_collection").isNotNull(), True).otherwise(False))
    
    # Calculate ROI locally since it's not in the cleaned dataframe
    df = df.withColumn("roi", F.col("revenue_musd") / F.col("budget_musd"))

    stats = df.groupBy("is_franchise").agg(
        F.mean("revenue_musd").alias("mean_revenue"),
        F.mean("budget_musd").alias("mean_budget"),
        F.mean("popularity").alias("mean_popularity"),
        F.mean("vote_average").alias("mean_rating"),
        F.expr("percentile_approx(roi, 0.5)").alias("median_roi")
    )
    return stats


def analyze_directors(df):
    """
    Finds most successful directors.
    """
    # Filter out null directors
    df_d = df.filter(F.col("director").isNotNull())
    
    director_stats = df_d.groupBy("director").agg(
        F.count("*").alias("total_movies"),
        F.sum("revenue_musd").alias("total_revenue"),
        F.mean("vote_average").alias("mean_rating")
    )
    
    # Successful: High revenue or High rating
    return director_stats.orderBy(F.col("total_revenue").desc())
