from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, 
    DoubleType, LongType, ArrayType, BooleanType, DateType
)


# RAW MOVIE API SCHEMA
# ---------------------------------------------------------------------------
# Defines the structure of the JSON response from TMDB (Details + Credits)

# Sub-structures for nested arrays
genre_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True)
])

company_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("logo_path", StringType(), True),
    StructField("origin_country", StringType(), True)
])

country_schema = StructType([
    StructField("iso_3166_1", StringType(), True),
    StructField("name", StringType(), True)
])

language_schema = StructType([
    StructField("english_name", StringType(), True),
    StructField("iso_639_1", StringType(), True),
    StructField("name", StringType(), True)
])

collection_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("poster_path", StringType(), True),
    StructField("backdrop_path", StringType(), True)
])

# Cast and Crew (inside 'credits')
# Cast and Crew (inside 'credits')
cast_member_schema = StructType([
    StructField("adult", BooleanType(), True),
    StructField("cast_id", LongType(), True),
    StructField("character", StringType(), True),
    StructField("credit_id", StringType(), True),
    StructField("gender", LongType(), True),
    StructField("id", LongType(), True),
    StructField("known_for_department", StringType(), True),
    StructField("name", StringType(), True),
    StructField("order", LongType(), True),
    StructField("original_name", StringType(), True),
    StructField("popularity", DoubleType(), True),
    StructField("profile_path", StringType(), True)
])

crew_member_schema = StructType([
    StructField("adult", BooleanType(), True),
    StructField("credit_id", StringType(), True),
    StructField("department", StringType(), True),
    StructField("gender", LongType(), True),
    StructField("id", LongType(), True),
    StructField("job", StringType(), True),
    StructField("known_for_department", StringType(), True),
    StructField("name", StringType(), True),
    StructField("original_name", StringType(), True),
    StructField("popularity", DoubleType(), True),
    StructField("profile_path", StringType(), True)
])

credits_schema = StructType([
    StructField("cast", ArrayType(cast_member_schema), True),
    StructField("crew", ArrayType(crew_member_schema), True)
])

# Main Movie Schema
raw_movie_schema = StructType([
    StructField("adult", BooleanType(), True),
    StructField("backdrop_path", StringType(), True),
    StructField("belongs_to_collection", collection_schema, True),
    StructField("budget", LongType(), True),
    StructField("genres", ArrayType(genre_schema), True),
    StructField("homepage", StringType(), True),
    StructField("id", LongType(), True),
    StructField("imdb_id", StringType(), True),
    StructField("original_language", StringType(), True),
    StructField("original_title", StringType(), True),
    StructField("overview", StringType(), True),
    StructField("popularity", DoubleType(), True),
    StructField("poster_path", StringType(), True),
    StructField("production_companies", ArrayType(company_schema), True),
    StructField("production_countries", ArrayType(country_schema), True),
    StructField("release_date", StringType(), True),  # Ingest as string, cast to date later
    StructField("revenue", LongType(), True),
    StructField("runtime", IntegerType(), True),
    StructField("spoken_languages", ArrayType(language_schema), True),
    StructField("status", StringType(), True),
    StructField("tagline", StringType(), True),
    StructField("title", StringType(), True),
    StructField("video", BooleanType(), True),
    StructField("vote_average", DoubleType(), True),
    StructField("vote_count", LongType(), True),
    # Nested field added during ingestion
    StructField("credits", credits_schema, True) 
])
