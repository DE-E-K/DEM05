
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, FloatType


def clean_dataframe(df):
    """
    Cleans and preprocesses the movie dataframe.

    Args:
        df: Raw Spark DataFrame.

    Returns:
        DataFrame: Cleaned and transformed DataFrame.
    """
    print("Starting data cleaning...")

    # 1. Drop irrelevant columns
    columns_to_drop = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
    df_dropped = df.drop(*columns_to_drop)

    # 2. Extract key data points from JSON-like columns
    # Assuming 'genres' is an array of structs or JSON string.
    # If inferred from API JSON, basic schema should be ArrayType(StructType)
    # genres -> extract 'name' and join with '|'

    # This UDF or expression complexity depends on how Spark inferred the schema.
    # We will assume standard JSON inference where 'genres' is Array<Struct<id:long, name:string>>

    # Genres
    if 'genres' in df_dropped.columns:
        df_dropped = df_dropped.withColumn("genres", F.expr("transform(genres, x -> x.name)"))
        df_dropped = df_dropped.withColumn("genres", F.concat_ws("|", "genres"))

    # Spoken Languages
    if 'spoken_languages' in df_dropped.columns:
        df_dropped = df_dropped.withColumn("spoken_languages", F.expr("transform(spoken_languages, x -> x.name)"))
        df_dropped = df_dropped.withColumn("spoken_languages", F.concat_ws("|", "spoken_languages"))

    # Production Countries
    if 'production_countries' in df_dropped.columns:
        df_dropped = df_dropped.withColumn("production_countries", F.expr("transform(production_countries, x -> x.name)"))
        df_dropped = df_dropped.withColumn("production_countries", F.concat_ws("|", "production_countries"))

    # Production Companies
    if 'production_companies' in df_dropped.columns:
        df_dropped = df_dropped.withColumn("production_companies", F.expr("transform(production_companies, x -> x.name)"))
        df_dropped = df_dropped.withColumn("production_companies", F.concat_ws("|", "production_companies"))

    # Collection Name (belongs_to_collection is likely a Struct)
    if 'belongs_to_collection' in df_dropped.columns:
        df_dropped = df_dropped.withColumn("belongs_to_collection", F.col("belongs_to_collection.name"))

    # 3. Handle Datatypes and Missing Values

    # Convert budget and revenue to millions (assuming they are numeric, otherwise cast first)
    # Check if budget/revenue are 0 -> replace with NaN or leave as is based on instruction "Replace with NaN or..."
    # We will use Spark's 'NaN' for float columns or null for others.

    df_clean = df_dropped.withColumn("budget", F.col("budget").cast(FloatType())) \
                         .withColumn("revenue", F.col("revenue").cast(FloatType())) \
                         .withColumn("vote_count", F.col("vote_count").cast(IntegerType())) \
                         .withColumn("vote_average", F.col("vote_average").cast(FloatType())) \
                         .withColumn("popularity", F.col("popularity").cast(FloatType())) \
                         .withColumn("runtime", F.col("runtime").cast(IntegerType()))

    # Release Date
    df_clean = df_clean.withColumn("release_date", F.to_date(F.col("release_date"), "yyyy-MM-dd"))

    # Replace 0 with NaN (Null in Spark usually serves this purpose better for SQL ops, but we can use NaN for floats)
    # Requirement: "Budget/Revenue/Runtime = 0 -> Replace with NaN"
    # Note: Spark SQL does support 'NaN' for Double/Float.

    df_clean = df_clean.withColumn("budget", F.when(F.col("budget") == 0, F.lit(None)).otherwise(F.col("budget")))
    df_clean = df_clean.withColumn("revenue", F.when(F.col("revenue") == 0, F.lit(None)).otherwise(F.col("revenue")))
    df_clean = df_clean.withColumn("runtime", F.when(F.col("runtime") == 0, F.lit(None)).otherwise(F.col("runtime")))

    # Convert to Musd
    df_clean = df_clean.withColumn("budget_musd", F.col("budget") / 1000000)
    df_clean = df_clean.withColumn("revenue_musd", F.col("revenue") / 1000000)

    # 4. Filter 'Released' movies
    if 'status' in df_clean.columns:
        df_clean = df_clean.filter(F.col("status") == "Released")
        # Reuse df_clean to drop status after filter
        df_clean = df_clean.drop("status")

    # 5. Remove duplicates and rows with unknown ID/Title
    df_clean = df_clean.dropDuplicates(['id'])
    df_clean = df_clean.filter(F.col("id").isNotNull() & F.col("title").isNotNull())

    # 6. Keep rows with at least 10 non-null columns (using a check of how many columns are not null)
    # This is expensive in Spark, but we can do it with an expression

    cols_to_check = df_clean.columns
    # Create an expression that sums up 1 for every NOT NULL column
    non_null_count_expr = sum(F.when(F.col(c).isNotNull(), 1).otherwise(0) for c in cols_to_check)
    df_clean = df_clean.withColumn("non_null_count", non_null_count_expr)
    df_clean = df_clean.filter(F.col("non_null_count") >= 10)
    df_clean = df_clean.drop("non_null_count")

    # 7. Reorder columns as specified in the instructions
    """['id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection', 'original_language', 
    'budget_musd', 'revenue_musd', 'production_companies', 'production_countries', 'vote_count', 
    'vote_average', 'popularity', 'runtime', 'overview', 'spoken_languages', 'poster_path', 
    'cast', 'cast_size', 'director', 'crew_size']"""

    df_clean = df_clean.select(['id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection', 'original_language', 
    'budget_musd', 'revenue_musd', 'production_companies', 'production_countries', 'vote_count', 
    'vote_average', 'popularity', 'runtime', 'overview', 'spoken_languages', 'poster_path', 
    'cast', 'cast_size', 'director', 'crew_size'])

    print("Data cleaning completed.")
    return df_clean
