# Real-Time E-Commerce Data Ingestion Project Overview

## Executive Summary

This project implements a **production-grade real-time data pipeline** that ingests e-commerce events from CSV files, processes them using Apache Spark Structured Streaming, and persists them in PostgreSQL. The pipeline demonstrates enterprise-level streaming architecture with data validation, deduplication, and error handling.

## Problem Statement

Modern e-commerce platforms generate continuous streams of user events (views, purchases, cart actions). Traditional batch processing introduces latency and misses real-time insights. This project solves the need for:

- **Real-time ingestion** of event data
- **Scalable processing** with Apache Spark
- **Reliable storage** in PostgreSQL
- **Performance monitoring** and validation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Data Generator (Python)                    │
│         Generates fake e-commerce events as CSV files           │
└────────────────────────┬────────────────────────────────────────┘
                         │ CSV files
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    data/input_data/ Directory                   │
│              (Monitored for new CSV file arrivals)              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         Spark Structured Streaming (Scala/Python)               │
│    • Reads new CSV files as they arrive                         │
│    • Validates schema (7 columns)                               │
│    • Deduplicates events by event_id                            │
│    • Filters null values                                        │
│    • Trigger interval: 30 seconds                               │
└────────────────────────┬────────────────────────────────────────┘
                         │ Processed batches
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            PostgreSQL Database (ecommerce_streaming)            │
│    Table: events                                                │
│    • event_id (UUID, PRIMARY KEY)                               │
│    • event_type (VARCHAR)                                       │
│    • product_id (VARCHAR)                                       │
│    • user_id (VARCHAR)                                          │
│    • event_timestamp (TIMESTAMP)                                │
│    • quantity (INTEGER)                                         │
│    • price (NUMERIC)                                            │
│    • created_at (TIMESTAMP, auto-managed)                       │
│                                                                 │
│    Indexes: event_type, user_id, product_id, event_timestamp    │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Data Generation** | Python 3.8+ | 3.8+ | Simulates e-commerce events |
| **Stream Processing** | Apache Spark | 3.5.0 | Real-time data transformation |
| **Database** | PostgreSQL | 12+ | Persistent event storage |
| **JDBC Driver** | postgresql-42.7.3.jar | 42.7.3 | Spark-to-PostgreSQL connection |
| **Monitoring** | Spark UI + Logs | Built-in | Performance tracking |

## Key Features

### 1. **Continuous Data Generation**
- Generates realistic e-commerce events (view, purchase, add_to_cart, remove_from_cart)
- Configurable record count and generation intervals
- 50 products, 500 user IDs for realistic data distribution
- Timestamps in standardized format: `YYYY-MM-DD HH:MM:SS`

### 2. **Scalable Stream Processing**
- Structured Streaming for fault-tolerant processing
- Exactly-once semantics via checkpoint mechanism
- 30-second micro-batches for near real-time processing
- Automatic schema inference with custom validation

### 3. **Data Quality**
- **Deduplication**: Removed duplicate events by `event_id`
- **Null filtering**: Rejects records with null event_id
- **Type validation**: Enforces correct data types
- **Error handling**: Graceful failure with detailed logging

### 4. **Reliable Persistence**
- Transaction support from Spark JDBC driver
- Batch inserts for performance (1000 records per batch)
- Primary key constraint prevents duplicates in database
- Automatic index creation for query optimization

### 5. **Observability & Monitoring**
- Structured logging in both Python and Spark
- Batch-level processing metrics
- Checkpoint tracking for recovery
- Performance metrics collection (latency, throughput, error rates)

## Project Structure

```
Real_streaming/
├── src/
│   ├── data_generator.py              # Event generation script
│   ├── spark_streaming_to_postgres.py # Main streaming job
│   ├── reset_spark_process.py         # Table reset utility
│   └── requirements.txt               # Python dependencies
├── data/
│   ├── input_data/                    # CSV event files (generated)
│   └── checkpoint/                    # Spark checkpoint directory
├── config/
│   ├── postgres_setup.sql             # Database initialization
│   └── postgres_connection_details.txt# Connection credentials
├── docs/
│   ├── project_overview.md            # This file
│   ├── user_guide.md                  # Setup & execution guide
│   ├── test_cases.md                  # Manual test plan
│   ├── performance_metrics.md         # Metrics & benchmarks
│   ├── system_architecture.txt        # Architecture description
│   ├── walkthrough.md                 # Step-by-step walkthrough
│   └── folder_structure.md            # Directory structure
├── lib/
│   └── postgresql-42.7.3.jar          # PostgreSQL JDBC driver
├── tests/
│   └── (test scripts)
└── README.md                          # Project README
```

## Data Flow

1. **Generation Phase**
   - `data_generator.py` runs continuously
   - Creates CSV files every N seconds (configurable)
   - Each file contains 10-100 records (configurable)
   - Writes to `data/input_data/` directory

2. **Detection Phase**
   - Spark monitors `data/input_data/` directory
   - Automatically detects new CSV files
   - Reads headers and data with defined schema

3. **Processing Phase**
   - Validates schema conformance
   - Filters null event_ids
   - Deduplicates by event_id
   - Accumulates records in micro-batches

4. **Storage Phase**
   - Every 30 seconds, writes batch to PostgreSQL
   - Uses JDBC connection pool
   - Executes batch insert (1000 records/batch)
   - Logs success/failure for each batch

5. **Recovery Phase**
   - Checkpoint state tracked in `data/checkpoint/`
   - On restart, resumes from last checkpoint
   - No data loss or duplication

## Performance Characteristics

- **Latency**: 30-60 seconds from CSV creation to database persistence
- **Throughput**: 50-500 events/second depending on configuration
- **Batch Size**: Configurable (default 10-100 records/file)
- **Processing Time**: <1 second for typical micro-batch
- **Memory Footprint**: ~2GB Spark driver + 1GB PostgreSQL overhead

## Error Handling

| Error Scenario | Handling | Recovery |
|---|---|---|
| Missing CSV column | Schema validation fails, logs error | Skip batch, continue |
| Invalid timestamp | Type coercion fails | Application restarts from checkpoint |
| Database connection lost | Write fails, exception logged | Retry on next batch |
| Duplicate event_id | Caught by dropDuplicates() | Filtered before DB insert |
| Malformed CSV | Spark parser error | Skip file, continue |

## Security Considerations

- Database credentials stored in `postgres_connection_details.txt`
- Production: Use environment variables or secrets management
- JDBC connection over localhost (dev) or encrypted tunnel (prod)
- PostgreSQL user with minimal required privileges
- Input validation via schema enforcement

## Extensions & Enhancements

Future improvements:

- [ ] Kafka integration for higher-throughput ingestion
- [ ] Data quality metrics (null %, type mismatch %)
- [ ] Advanced transformations (enrichment, aggregations)
- [ ] Multi-sink support (S3, Snowflake, Iceberg)
- [ ] ML-driven anomaly detection
- [ ] Web dashboard for monitoring
- [ ] Alerting on SLA violations

## Success Criteria

* CSV files generated correctly with all required columns
* Spark detects new files automatically
* Data transformations execute without errors
* All records persisted in PostgreSQL
* Performance metrics meet latency SLAs
* No data loss on failure (checkpoint recovery)
* Logging provides operational visibility

## Lessons Learned

This project demonstrates:

- **Stream processing fundamentals** with Spark Structured Streaming
- **Enterprise-grade architecture** patterns (deduplication, checkpointing)
- **Database integration** for reliable data persistence
- **Operational excellence** with monitoring and logging
- **Scalability** through micro-batch processing

## Next Steps

1. **Setup**: Follow [user_guide.md](user_guide.md)
2. **Testing**: Execute test cases from [test_cases.md](test_cases.md)
3. **Monitoring**: Track metrics in [performance_metrics.md](performance_metrics.md)
4. **Production**: Adapt for cloud deployment (AWS, GCP, Azure)

---

**Last Updated**: February 2026  
**Maintainer**: Data Engineer
