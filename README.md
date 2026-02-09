# DEM05: Big Data, Data Processing, and Pipelines

This repository contains comprehensive coursework for the **DEM05 module** covering Big Data technologies, data processing frameworks, and pipeline development. The module consists of two major projects demonstrating practical applications of modern data engineering tools and methodologies.

## 📚 Module Overview

This module explores:
- **Batch Processing**: Data extraction, transformation, and analysis using Python and Apache Spark
- **Stream Processing**: Real-time data ingestion and processing with Spark Structured Streaming
- **Data Storage**: Working with both file systems and relational databases (PostgreSQL)
- **API Integration**: Extracting data from RESTful APIs
- **Data Engineering Best Practices**: Code modularity, testing, documentation, and version control

---

## 🎯 Projects

### Project 1: TMDB Movie Data Analysis
**Objective**: Build a comprehensive movie data analysis pipeline using APIs, Pandas, and Apache Spark.

#### Implementations:
- **[Python Implementation](TMDB-project/Python-impl/)** - Pandas-based ETL pipeline
- **[Spark Implementation](TMDB-project/Spark-impl/)** - PySpark distributed processing

#### Key Features:
- API data extraction from The Movie Database (TMDB)
- Complex data cleaning and transformation
- Financial analysis (ROI, profit, revenue trends)
- Franchise vs. standalone movie comparisons
- Director performance metrics
- Professional visualizations and insights

#### Technologies:
`Python` | `Pandas` | `Apache Spark` | `TMDB API` | `Matplotlib` | `Seaborn`

📖 **[View TMDB Project Details →](TMDB-project/)**

---

### Project 2: Real-Time Streaming Pipeline
**Objective**: Build a real-time data ingestion pipeline simulating e-commerce event tracking.

#### Key Features:
- Simulated streaming data generation
- Real-time processing with Spark Structured Streaming
- PostgreSQL database integration
- Checkpoint management and fault tolerance
- Performance monitoring and testing
- Comprehensive documentation

#### Technologies:
`Apache Spark Structured Streaming` | `PostgreSQL` | `Python` | `JDBC` | `CSV Streaming`

📖 **[View Streaming Project Details →](Real_streaming/)**

---

## 📂 Repository Structure

```
DEM05/
│
├── README.md                          # This file - Module overview
│
├── TMDB-project/                      # Project 1: Movie Data Analysis
│   ├── README.md                      # TMDB project overview
│   │
│   ├── Python-impl/                   # Pandas implementation
│   │   ├── main.py                    # Pipeline entry point
│   │   ├── requirements.txt           # Python dependencies
│   │   ├── README.md                  # Implementation guide
│   │   ├── data/                      # Raw and cleaned datasets
│   │   ├── models/                    # ETL modules
│   │   ├── plots/                     # Generated visualizations
│   │   └── kpi_report.txt            # Analysis results
│   │
│   └── Spark-impl/                    # PySpark implementation
│       ├── main.py                    # Spark pipeline entry
│       ├── requirements.txt           # Spark dependencies
│       ├── README.md                  # Spark implementation guide
│       ├── data/                      # Dataset storage
│       ├── model/                     # Spark modules
│       ├── notebooks/                 # Jupyter notebooks
│       └── output/                    # Processing results
│
└── Real_streaming/                    # Project 2: Real-Time Pipeline
    ├── README.md                      # Streaming project overview
    ├── requirements.txt               # Python + Spark dependencies
    │
    ├── config/                        # Configuration files
    │   ├── postgres_setup.sql         # Database schema
    │   └── postgres_connection_details.txt
    │
    ├── src/                           # Source code
    │   ├── data_generator.py          # Event simulator
    │   ├── spark_streaming_to_postgres.py  # Streaming job
    │   └── reset_spark_process.py     # Utility scripts
    │
    ├── data/                          # Data storage
    │   ├── input_data/                # Generated CSV events
    │   └── checkpoint/                # Spark checkpoints
    │
    ├── docs/                          # Documentation
    │   ├── project_overview.md
    │   ├── user_guide.md
    │   ├── test_cases.md
    │   ├── performance_metrics.md
    │   └── system_architecture.txt
    │
    └── tests/                         # Test suites
        ├── test_data_generation.py
        ├── test_spark_job.py
        └── test_db_connection.py
```

---

## 🚀 Getting Started

### Prerequisites

#### For TMDB Projects:
```bash
# Python 3.8+
python --version

# Java 8+ (for Spark implementation)
java -version
```

#### For Streaming Project:
```bash
# Python 3.8+
# Apache Spark 3.x
# PostgreSQL 12+
```

### Installation Guide

#### 1. Clone the Repository
```bash
git clone https://github.com/DE-E-K/DEM05.git
cd DEM05
```

#### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 3. Install Dependencies

**For TMDB Python Implementation:**
```bash
cd TMDB-project/Python-impl
pip install -r requirements.txt
```

**For TMDB Spark Implementation:**
```bash
cd TMDB-project/Spark-impl
pip install -r requirements.txt
```

**For Streaming Project:**
```bash
cd Real_streaming
pip install -r requirements.txt
```

---

## 🎓 Learning Outcomes

By completing this module, you will have demonstrated:

### Technical Skills
- ✅ **API Integration**: Fetching and handling REST API data
- ✅ **Data Cleaning**: Processing complex nested JSON structures
- ✅ **ETL Pipeline Development**: Building robust extraction, transformation, and loading workflows
- ✅ **Batch Processing**: Using Pandas and Spark for large-scale data analysis
- ✅ **Stream Processing**: Implementing real-time data pipelines with Spark Structured Streaming
- ✅ **Database Integration**: Connecting Spark to PostgreSQL via JDBC
- ✅ **Data Visualization**: Creating meaningful charts and reports
- ✅ **Testing**: Writing comprehensive test suites
- ✅ **Performance Optimization**: Measuring and improving system performance

### Professional Skills
- ✅ **Version Control**: Git best practices and branch management
- ✅ **Documentation**: Writing clear technical documentation
- ✅ **Code Organization**: Structuring projects for maintainability
- ✅ **Problem Solving**: Debugging and troubleshooting complex systems
- ✅ **System Design**: Architecting end-to-end data solutions

---

## 📊 Project Deliverables

### TMDB Project
- [x] Complete ETL pipeline (Python and Spark implementations)
- [x] Cleaned and processed datasets
- [x] KPI analysis reports
- [x] Professional visualizations
- [x] Comprehensive documentation
- [x] Source code with modular design

### Streaming Project
- [x] Data generation script
- [x] Spark Structured Streaming job
- [x] PostgreSQL database setup
- [x] System architecture diagram
- [x] Performance metrics report
- [x] Test cases and validation
- [x] User guide and documentation

---

## 🧪 Testing

Each project includes comprehensive testing:

### TMDB Project Testing
```bash
cd TMDB-project/Python-impl
python -m pytest tests/
```

### Streaming Project Testing
```bash
cd Real_streaming
pytest tests/ -v
```

---

## 📈 Performance Metrics

### TMDB Project
- API extraction speed with multiprocessing
- Data cleaning efficiency
- Memory usage optimization
- Visualization rendering time

### Streaming Project
- **Throughput**: Events processed per second
- **Latency**: End-to-end processing time
- **Reliability**: Checkpoint and recovery testing
- **Database Performance**: Insert rates and query efficiency

---

## 🛠️ Technologies Used

| Technology | Purpose | Projects |
|------------|---------|----------|
| **Python** | Primary programming language | Both |
| **Pandas** | Data manipulation and analysis | TMDB |
| **Apache Spark** | Distributed data processing | Both |
| **PySpark** | Python API for Spark | Both |
| **PostgreSQL** | Relational database | Streaming |
| **Matplotlib/Seaborn** | Data visualization | TMDB |
| **TMDB API** | Movie data source | TMDB |
| **JDBC** | Database connectivity | Streaming |
| **pytest** | Testing framework | Both |

---

## 📖 Documentation

### TMDB Project Documentation
- [Python Implementation README](TMDB-project/Python-impl/README.md)
- [Spark Implementation README](TMDB-project/Spark-impl/README.md)
- [Setup Guide](TMDB-project/Spark-impl/SETUP_GUIDE.txt)
- [Pipeline Walkthrough Notebook](TMDB-project/Python-impl/pipeline_walkthrough.ipynb)

### Streaming Project Documentation
- [Project Overview](Real_streaming/docs/project_overview.md)
- [User Guide](Real_streaming/docs/user_guide.md)
- [Test Cases](Real_streaming/docs/test_cases.md)
- [Performance Metrics](Real_streaming/docs/performance_metrics.md)
- [System Architecture](Real_streaming/docs/system_architecture.txt)
- [Folder Structure](Real_streaming/docs/folder_structure.md)
- [Walkthrough](Real_streaming/docs/walkthrough.md)

---

## 🌟 Key Highlights

### Data Engineering Best Practices Demonstrated
1. **Modular Code Architecture**: Separation of concerns (extraction, cleaning, analysis)
2. **Error Handling**: Robust exception handling and logging
3. **Configuration Management**: External configuration files for database connections
4. **Testing Strategy**: Unit tests, integration tests, and performance tests
5. **Documentation**: Comprehensive READMEs, inline comments, and user guides
6. **Version Control**: Git workflow with feature branches
7. **Performance Monitoring**: Metrics collection and analysis
8. **Scalability**: Designed for both small-scale and distributed processing

---

## 🔄 Git Workflow

This repository uses a branch-based workflow:

- `main` - Production-ready consolidated code
- `tmdb_project` - TMDB project development
- `python_impl` - Python/Pandas implementation
- `spark_impl` - Spark implementation
- `streaming` - Streaming project development

### Branch Consolidation
All branches have been merged into `main` for final submission with proper project organization.

---

## 🤝 Contributing

While this is a coursework project, contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is created for educational purposes as part of the DEM05 module coursework.

---

## 👨‍💻 Author

**DE-E-K**

- GitHub: [@DE-E-K](https://github.com/DE-E-K)
- Repository: [DEM05](https://github.com/DE-E-K/DEM05.git)

---

## 📞 Support

For questions or issues:
1. Check the project-specific README files
2. Review the documentation in `docs/` folders
3. Examine the test cases for usage examples
4. Raise an issue on GitHub

---

## 🎯 Next Steps

To extend these projects, consider:

### TMDB Enhancements
- [ ] Add more visualization types
- [ ] Implement machine learning models for prediction
- [ ] Create interactive dashboards
- [ ] Expand to more API sources

### Streaming Enhancements
- [ ] Add Kafka for message queuing
- [ ] Implement Redis for caching
- [ ] Add monitoring with Grafana
- [ ] Deploy on cloud infrastructure (AWS/Azure)
- [ ] Add data validation and quality checks
- [ ] Implement alerting mechanisms

---

## 📅 Project Timeline

- **Phase 1**: API Integration and Data Extraction
- **Phase 2**: Data Cleaning and Transformation
- **Phase 3**: Analysis and KPI Implementation
- **Phase 4**: Streaming Pipeline Development
- **Phase 5**: Testing and Performance Optimization
- **Phase 6**: Documentation and Finalization

---

**Built with for Data Engineering Excellence**
