# TMDB Movie Data Analysis Project

This project demonstrates comprehensive data engineering skills through the analysis of movie data from The Movie Database (TMDB) API. The project is implemented in two different approaches to showcase both traditional data analysis (Pandas) and big data processing (Apache Spark).

## 🎬 Project Overview

**Objective**: Build a complete movie data analysis pipeline that extracts, cleans, transforms, and analyzes movie data to derive meaningful business insights.

**Data Source**: [The Movie Database (TMDB) API](https://www.themoviedb.org/)

## 📊 Project Aims

This project fulfills the following requirements:

1. **API Data Extraction**: Fetch movie-related data from TMDB API
2. **Data Cleaning & Transformation**: Process complex JSON structures and prepare data for analysis
3. **Exploratory Data Analysis (EDA)**: Understand trends and patterns in movie data
4. **Advanced Filtering & Ranking**: Identify top performers based on various metrics
5. **Franchise & Director Analysis**: Assess performance across movie franchises and directors
6. **Visualization & Insights**: Present findings through professional visualizations

## 🔧 Two Implementations

### 1. Python + Pandas Implementation

**Best for**: Small to medium datasets, rapid prototyping, detailed analysis

**Location**: [`Python-impl/`](Python-impl/)

**Key Features**:
- Efficient API data extraction with multiprocessing
- Advanced Pandas transformations
- Rich visualizations with Matplotlib and Seaborn
- Comprehensive KPI reporting
- Optimized for single-machine processing

**Technologies**:
- Python 3.8+
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Requests

📖 **[View Python Implementation →](Python-impl/)**

---

### 2. Apache Spark Implementation

**Best for**: Large-scale datasets, distributed processing, production environments

**Location**: [`Spark-impl/`](Spark-impl/)

**Key Features**:
- Distributed data processing with PySpark
- Scalable transformations
- Optimized for big data workflows
- Production-ready pipeline
- Supports cluster deployment

**Technologies**:
- Apache Spark 3.3
- PySpark
- Python 3.8+
- Java 17

📖 **[View Spark Implementation →](Spark-impl/)**

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# For Spark implementation: Java 8 or higher
java -version
```

### Setup

#### Python Implementation
```bash
cd Python-impl
pip install -r requirements.txt
python main.py
```

#### Spark Implementation
```bash
cd Spark-impl
pip install -r requirements.txt
```

## 📈 Key Features & Capabilities

### Data Extraction
- ✅ Fetch movie metadata for specific movie IDs
- ✅ Robust error handling and retry logic
- ✅ Parallel processing for faster extraction
- ✅ Cast and crew information extraction

### Data Cleaning & Preprocessing
- ✅ Drop irrelevant columns
- ✅ Parse complex JSON structures (genres, production companies, cast, crew)
- ✅ Handle missing and incorrect data
- ✅ Convert data types appropriately
- ✅ Remove duplicates
- ✅ Filter for data quality (minimum non-null values)

### Analysis & KPIs

#### Performance Metrics
1. **Financial Analysis**
   - Highest/Lowest Revenue
   - Highest/Lowest Budget
   - Highest/Lowest Profit (Revenue - Budget)
   - Highest/Lowest ROI (Return on Investment)

2. **Popularity & Ratings**
   - Most Voted Movies
   - Highest/Lowest Rated Movies
   - Most Popular Movies

3. **Advanced Filtering**
   - Genre-specific searches
   - Actor-specific queries
   - Director-specific analysis
   - Multi-criteria filtering

4. **Franchise Analysis**
   - Franchise vs. Standalone comparison
   - Mean Revenue, ROI, Budget, Popularity, Rating
   - Most successful franchises

5. **Director Analysis**
   - Total movies directed
   - Total and mean revenue
   - Average ratings

### Visualizations
- 📊 Revenue vs. Budget trends
- 📈 ROI distribution by genre
- ⭐ Popularity vs. Rating correlations
- 📅 Yearly box office performance
- 🎬 Franchise vs. Standalone comparisons

## 🗂️ Data Pipeline

```
┌─────────────────┐
│  TMDB API       │
│  (Raw Data)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extraction     │
│  (Python/Spark) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cleaning       │
│  & Transform    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Analysis       │
│  & KPIs         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualization  │
│  & Reporting    │
└─────────────────┘
```

## 📋 Deliverables

Both implementations provide:

| Deliverable | Description |
|-------------|-------------|
| **Complete Pipeline** | End-to-end workflow from API to insights |
| **Cleaned Dataset** | Production-ready movie data |
| **KPI Report** | Comprehensive analysis of key metrics |
| **Visualizations** | Professional charts and graphs |
| **Documentation** | README, code comments, user guides |
| **Source Code** | Modular, maintainable, well-structured |

## 🎯 Sample Movies Analyzed

The project analyzes movies with the following IDs:
```python
movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 
             168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 
             321612, 260513]
```

This includes popular franchises and standalone films to enable meaningful comparative analysis.

## 📚 Sample Queries Answered

### Business Questions
1. **Which movie franchise generates the highest revenue?**
2. **What is the ROI for Science Fiction movies?**
3. **Which directors have the highest average ratings?**
4. **How do franchise movies compare to standalone films in terms of profitability?**
5. **What are the trends in movie budgets over time?**

### Advanced Filters
- Best-rated Science Fiction Action movies starring Bruce Willis
- Movies starring Uma Thurman directed by Quentin Tarantino
- High-budget movies with low ROI

## 🔍 Data Schema

### Source Columns (from API)
- Movie metadata: id, title, tagline, release_date, runtime
- Financial: budget, revenue
- Ratings: vote_count, vote_average, popularity
- Content: overview, genres, original_language
- Collections: belongs_to_collection
- Production: production_companies, production_countries
- Cast & Crew: cast, crew, director

### Processed Columns
```
['id', 'title', 'tagline', 'release_date', 'genres', 
 'belongs_to_collection', 'original_language', 'budget_musd', 
 'revenue_musd', 'production_companies', 'production_countries', 
 'vote_count', 'vote_average', 'popularity', 'runtime', 
 'overview', 'spoken_languages', 'poster_path', 'cast', 
 'cast_size', 'director', 'crew_size']
```

## 🧪 Testing

Run tests to validate data quality and pipeline functionality:

```bash
# Python implementation
cd Python-impl
pytest tests/

# Spark implementation
cd Spark-impl
pytest tests/
```

## 📊 Performance Comparison

| Metric | Python/Pandas | Apache Spark |
|--------|---------------|--------------|
| **Dataset Size** | < 10GB | 10GB - Petabytes |
| **Processing Speed** | Fast for small data | Optimized for big data |
| **Memory Usage** | Single machine RAM | Distributed memory |
| **Scalability** | Vertical (more RAM) | Horizontal (more nodes) |
| **Development Speed** | Faster prototyping | Requires more setup |
| **Best Use Case** | Analysis & reporting | Production pipelines |

## 🌟 Key Learning Outcomes

By completing this project, you will learn:

- ✅ **API Integration**: Fetching and handling REST API responses
- ✅ **Data Wrangling**: Cleaning messy, real-world data
- ✅ **JSON Processing**: Parsing nested structures
- ✅ **Data Transformation**: Type conversion, missing value handling
- ✅ **Aggregation**: Computing metrics across groups
- ✅ **Filtering**: Complex multi-condition queries
- ✅ **Visualization**: Creating meaningful charts
- ✅ **Code Organization**: Modular design and separation of concerns
- ✅ **Pandas Mastery**: Advanced DataFrame operations
- ✅ **Spark Fundamentals**: Distributed computing concepts

## 🔄 Choosing an Implementation

**Choose Python/Pandas if**:
- Working with datasets < 5GB
- Need rapid prototyping and exploration
- Prefer simpler setup and dependencies
- Focus is on analysis and visualization

**Choose Apache Spark if**:
- Dataset is > 10GB or growing rapidly
- Need to process data in parallel/distributed manner
- Preparing for production deployment
- Want to learn big data technologies

**Do both!** Compare the approaches and understand tradeoffs.

## 🛣️ Project Workflow

1. **Setup**: Install dependencies and configure API keys
2. **Extract**: Fetch movie data from TMDB API
3. **Clean**: Process and standardize the dataset
4. **Analyze**: Compute KPIs and perform queries
5. **Visualize**: Generate charts and reports
6. **Document**: Write findings and insights

## 📖 Additional Resources

- [TMDB API Documentation](https://developers.themoviedb.org/3)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Data Cleaning Best Practices](https://www.kaggle.com/learn/data-cleaning)

## 🤝 Contributing

Improvements and suggestions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is developed for educational purposes as part of the DEM05 coursework.
While I'm in apprenticeship at AmaliTech
