# TMDB Movie Data Analysis - Final Report

## 1. Project Overview
This project involved building a comprehensive data analysis pipeline for movie data fetched from the TMDb API. The goal was to extract insights regarding movie performance, financials, and trends using Python, Pandas, and visualization libraries. The analysis focused on a curated list of 18 high-profile movies.

## 2. Methodology

### Data Extraction
-   **Source**: Fetched data using the TMDb API.
-   **Scope**: Retrieved data for 19 target movie IDs (18 successfully fetched).
-   **Enrichment**: Used `append_to_response='credits'` to fetch detailed Cast and Crew information.

### Data Cleaning & Preprocessing
-   **Filtering**: 
    -   Dropped irrelevant columns (`adult`, `imdb_id`, `original_title`).
    -   Removed duplicates based on movie ID.
    -   Filtered for movies with `status == 'Released'`.
    -   Applied a threshold to keep rows with at least 10 non-missing values.
-   **Feature Extraction**:
    -   **JSON Parsing**: Flattened nested JSON in `genres`, `production_companies`, `production_countries`, and `spoken_languages`.
    -   **Crew Analysis**: Extracted Director names and calculated Cast/Crew sizes.
    -   **Financials**: Converted Budget and Revenue to Millions (USD) and calculated `Profit` and `ROI`.
    -   **Franchises**: extracted collection names to flag Franchise movies.
-   **Handling Missing Data**: Replaced unrealistic 0 values in financial and runtime columns with NaN to avoid skewing statistics.

## 3. Key Findings & Insights

### Financial Performance
-   **Budget vs Revenue**: Strong positive correlation observed. High investment generally yields high returns for this dataset.
-   **Top Performers**:
    -   **James Cameron** dominates with *Avatar* and *Titanic*, generating over **$5.1B** combined in this specific dataset.
    -   **The Avengers Collection** is a financial titan, amassing over **$7.7B** in revenue across 4 movies.

### Franchise Impact
-   **Franchise Dominance**: Franchise movies exhibit significantly higher **Mean Revenue** and **Popularity** compared to standalone films.
-   **Risk Reduction**: Franchises offer a more stable Return on Investment (ROI), acting as "cash cows" for studios. The *Avengers* and *Star Wars* collections are prime examples of this stability.

### Talent Impact (Directors)
-   **Revenue Drivers**: 
    -   **James Cameron**: Highest total revenue ($5.2B) from just 2 movies.
    -   **Joss Whedon**: ~$2.9B revenue.
    -   **Russo Brothers**: ~$2.8B revenue with high critical acclaim (Average Vote ~8.2).
-   **Success Rate**: Directors like the Russo Brothers and David Yates show a strong correlation between high critical ratings and box office success.

### Genres & Trends
-   **Top Genres**: **Adventure**, **Action**, and **Science Fiction** are the most prevalent and profitable genres.
-   **Yearly Growth**: Box office revenue demonstrates a clear upward trend over recent decades, driven by the rise of mega-franchises and inflation.

## 4. Deliverables
-   **Jupyter Notebook**: `tmdb_analysis.ipynb` (Code, Analysis, Visualizations).
-   **This Report**: `final_report.md` (Summary of Methodology and Findings).
-   **Raw Data**: `tmdb_movies_raw_data.csv`.

## 5. Conclusion
The analysis confirms that the modern film industry's financial success is heavily reliant on the **Franchise Model** and **Star Power** (both Cast and Directors).
-   **Franchises** like *The Avengers* provide a reliable, high-yield revenue stream.
-   **Visionary Directors** like James Cameron and the Russo Brothers are individual brands that guarantee blockbuster status.
-   **Action/Adventure/Sci-Fi** remains the "Golden Trinity" of genres for maximizing global box office reach.
