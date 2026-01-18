# TMDB Movie Data Analysis

## Project Overview
This project is a comprehensive data analysis of the modern film industry, exploring the factors that drive financial success and audience popularity. By leveraging the **The Movie Database (TMDb) API**, we enrich a dataset of high-profile movies with details on budgets, revenue, cast, crew, and production information to uncover actionable trends.

## Repository Structure

### Analysis & Reports
- **`tmdb_analysis.ipynb`**: The core Jupyter Notebook containing the full pipeline:
    -   **Data Extraction**: Fetching live data from TMDb API.
    -   **Data Cleaning**: Handling missing values, deduplication, and type conversion.
    -   **Feature Engineering**: Extracting franchise details, director names, and profitability metrics.
    -   **EDA**: Visualizing trends in budget, revenue, genres, and more.
- **`final_report.md`**: A concise summary of the project's methodology, key findings, and strategic conclusions.

### Data
- **`tmdb_movies_raw_data.csv`**: The raw data fetched directly from the API.
- **`tmdb_movies_cleaned.csv`**: The processed dataset used for analysis.

### Configuration
- **`.env`**: Configuration file for storing sensitive credentials (API Key).
- **`.gitignore`**: Specifies files to be ignored by version control.

## Key Analysis Areas
1.  **Financial Mechanics**: Correlation between production budget and box office revenue; Profitability and ROI analysis.
2.  **Franchise Power**: Comparing the performance and stability of franchise installments versus standalone films.
3.  **Talent Impact**: Evaluating the box office influence of top directors and cast size.
4.  **Genre Dynamics**: Identifying the most profitable and popular genres in the current market.

## Setup & Usage

### Prerequisites
-   Python 3.13.5
-   Jupyter Notebook

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/DE-E-K/DEM05.git
    cd DEM05
    ```

2.  **Install dependencies**:
    Ensure you have the following Python libraries installed:
    ```bash
    pip install pandas numpy matplotlib seaborn requests python-dotenv
    ```

3.  **API Key Configuration**:
    To fetch fresh data, you need a TMDb API key.
    -   Create a `.env` file in the root directory.
    -   Add your key:
        ```text
        API_KEY=your_tmdb_api_key_here
        ```

### Running the Analysis
1.  Launch Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
2.  Open `tmdb_analysis.ipynb`.
3.  Run the cells sequentially. The notebook is structured to load existing CSVs if they exist, or refetch data if configured to do so.

## Key Insights Teaser
*For detailed findings, please read [final_report.md](final_report.md).*

-   **High Investment, High Reward**: There is a strong positive correlation between budget and revenue.
-   **Franchises Rule**: Collection-based movies (e.g., *Avengers*, *Star Wars*) significantly outperform standalone films in both revenue and stability.
-   **Directorial Brand**: Visionary directors like James Cameron function as individual franchises, driving massive financial success.
