# User Guide: Real-Time E-Commerce Streaming Pipeline

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation & Setup](#installation--setup)
3. [Configuration](#configuration)
4. [Running the Pipeline](#running-the-pipeline)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Cleanup & Reset](#cleanup--reset)

---

## Prerequisites

### Required Software
- **Python 3.8+** - Data generation script
- **Apache Spark 3.0+** - Stream processing
- **PostgreSQL 12+** - Data storage
- **Java 8 or 11** - Required by Spark
- **Git** (optional) - For cloning repository

### System Requirements
- **RAM**: Minimum 8GB (Spark 4GB + PostgreSQL 2GB + OS 2GB)
- **Disk Space**: 5GB free space (for logs, data, checkpoints)
- **CPU**: Dual-core minimum (quad-core recommended)
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### Verify Prerequisites
```bash
# Check Python
python --version
# Expected: Python 3.8.x or higher

# Check Java
java -version
# Expected: java version "11.x.x" or "1.8.x"

# Check PostgreSQL
psql --version
# Expected: psql (PostgreSQL) 12.x or higher
```

---

## Installation & Setup

### Step 1: Install Python Dependencies

From the project root directory:

```bash
cd Real_streaming
pip install -r src/requirements.txt
```

**Expected output**:
```
Successfully installed pyspark-3.5.0 psycopg2-binary-2.9.11 python-dotenv-1.0.0
```

### Step 2: Verify PostgreSQL is Running

**On Windows (Command Prompt as Admin)**:
```bash
# Check PostgreSQL service
wmic service where name="postgresql-x64-12" get state

# Or use Services GUI
services.msc
```

**On macOS**:
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql
```

**On Linux**:
```bash
# Check PostgreSQL service
sudo systemctl status postgresql
```

### Step 3: Create the Database

Open PostgreSQL command line:

```bash
psql -U postgres -h localhost
```

Then run the setup script:

```bash
\i config/postgres_setup.sql
```

**Expected output**:
```
CREATE DATABASE
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
GRANT
GRANT
GRANT
 tablename         
────────────────
 events
(1 row)
```

Verify the table exists:

```bash
\c ecommerce_streaming
\dt
```

**Expected output**:
```
          List of relations
 Schema | Name  | Type  | Owner   
────────┼───────┼───────┼─────────
 public | events | table | postgres
(1 row)
```

Exit PostgreSQL:
```bash
\q
```

### Step 4: Verify Database Credentials

Edit `config/postgres_connection_details.txt` to match your setup:

```properties
host=localhost
port=5432
database=ecommerce_streaming
user=postgres
password=YOUR_PASSWORD_HERE
table=events
```

Test the connection with psql:
```bash
psql -h localhost -U postgres -d ecommerce_streaming -c "SELECT 1;"
```

**Expected output**:
```
 ?column? 
──────────
        1
(1 row)
```

### Step 5: Download PostgreSQL JDBC Driver (if not present)

The JDBC driver is needed for Spark to write to PostgreSQL.

#### Option A: Download manually
1. Visit [PostgreSQL JDBC Releases](https://jdbc.postgresql.org/download.html)
2. Download `postgresql-42.7.3.jar`
3. Place the JAR file in `lib/` directory

#### Option B: Use Maven (if installed)
```bash
mvn dependency:copy-dependencies -DoutputDirectory=lib -Dartifact=org.postgresql:postgresql:42.7.3
```

**Verify the JAR exists**:
```bash
ls lib/postgresql-42.7.3.jar  # Linux/macOS
dir lib\postgresql-42.7.3.jar  # Windows
```

---

## Configuration

### Data Generator Configuration

The data generator can be customized via command-line arguments:

```bash
python src/data_generator.py [OPTIONS]
```

**Available options**:

| Option | Default | Description |
|--------|---------|-------------|
| `--output-dir` | `../data/input_data` | Directory where CSV files are written |
| `--min-records` | `10` | Minimum records per CSV file |
| `--max-records` | `100` | Maximum records per CSV file |
| `--sleep` | `2` | Seconds to sleep between file generation |
| `--files` | `0` | Number of files to generate (0 = infinite) |

**Examples**:
```bash
# Generate CSV files continuously with default settings
python src/data_generator.py

# Generate 50 files with 100-200 records each, 5 seconds apart
python src/data_generator.py --min-records 100 --max-records 200 --sleep 5 --files 50

# Custom output directory
python src/data_generator.py --output-dir /tmp/events
```

### Spark Configuration

Edit `spark_streaming_to_postgres.py` to modify:

- **Trigger interval**: Change `processingTime="30 seconds"` to different value
- **Batch size**: Modify `batchsize` option (default 1000)
- **Partition count**: Adjust `spark.sql.shuffle.partitions` (default 4)

---

## Running the Pipeline

### Terminal 1: Start the Data Generator

```bash
cd Real_streaming
python src/data_generator.py --sleep 3 --files 0
```

**Expected output**:
```
2026-02-08 10:30:45,123 - INFO - ============================================================
2026-02-08 10:30:45,124 - INFO - Real-Time E-Commerce Data Generator
2026-02-08 10:30:45,125 - INFO - ============================================================
2026-02-08 10:30:45,126 - INFO - Output directory: C:\...\Real_streaming\data\input_data
2026-02-08 10:30:45,127 - INFO - Records per file: 10 - 100
2026-02-08 10:30:45,128 - INFO - Sleep interval: 3s
2026-02-08 10:30:45,129 - INFO - Files to generate: Infinite
2026-02-08 10:30:45,130 - INFO - ============================================================
2026-02-08 10:30:45,345 - INFO - ✓ Generated C:\...\Real_streaming\data\input_data\events_1707370245_0.csv with 47 records
```

**Keep this terminal running** and proceed to Terminal 2.

### Terminal 2: Start the Spark Streaming Job

In a **new terminal**:

```bash
cd Real_streaming
spark-submit --driver-class-path lib/postgresql-42.7.3.jar \
              --jars lib/postgresql-42.7.3.jar \
              src/spark_streaming_to_postgres.py
```

**Alternative (if above doesn't work)**:
```bash
spark-submit --packages org.postgresql:postgresql:42.7.3 \
              src/spark_streaming_to_postgres.py
```

**Expected output**:
```
2026-02-08 10:31:15,456 - INFO - ============================================================
2026-02-08 10:31:15,457 - INFO - Real-Time E-Commerce Streaming Pipeline
2026-02-08 10:31:15,458 - INFO - ============================================================
2026-02-08 10:31:15,459 - INFO - Monitoring directory: C:\...\Real_streaming\data\input_data
2026-02-08 10:31:15,460 - INFO - Database: ecommerce_streaming
2026-02-08 10:31:15,461 - INFO - Table: events
2026-02-08 10:31:15,462 - INFO - ============================================================
2026-02-08 10:31:15,465 - INFO - Streaming query started. Waiting for termination...
```

**Keep this terminal running** and proceed to Terminal 3.

### Terminal 3: Verify Data Flow

Open a third terminal and monitor the database:

```bash
cd Real_streaming
psql -h localhost -U postgres -d ecommerce_streaming
```

Inside PostgreSQL, run queries to monitor data flow:

**Count total records**:
```sql
SELECT COUNT(*) as total_events FROM events;
```

**View latest events**:
```sql
SELECT 
    event_id, 
    event_type, 
    product_id, 
    user_id, 
    event_timestamp 
FROM events 
ORDER BY event_timestamp DESC 
LIMIT 10;
```

**Count by event type**:
```sql
SELECT event_type, COUNT(*) as count 
FROM events 
GROUP BY event_type;
```

**Monitor in real-time** (PostgreSQL 12+):
```bash
watch -n 5 "psql -h localhost -U postgres -d ecommerce_streaming -c 'SELECT COUNT(*) FROM events;'"
```

---

## Verification

### Verification Checklist

| Step | Command | Expected Result |
|------|---------|-----------------|
| 1 | Check CSV generation | Files appear in `data/input_data/` every 3 seconds |
| 2 | Check Spark logs | See "Writing batch X to PostgreSQL..." messages |
| 3 | Count DB records | `SELECT COUNT(*) FROM events;` increases |
| 4 | Check data quality | `SELECT * FROM events LIMIT 1;` shows all 7 columns |
| 5 | Check deduplication | No duplicate event_ids in database |

### Sample Test Query

```sql
-- Comprehensive data verification
SELECT 
    event_type,
    COUNT(*) as count,
    COUNT(DISTINCT event_id) as unique_events,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT product_id) as unique_products,
    MIN(event_timestamp) as earliest,
    MAX(event_timestamp) as latest
FROM events
GROUP BY event_type;
```

**Expected output** (after 1 minute):
```
 event_type     | count  | unique_events | unique_users | unique_products | earliest | latest
────────────────┼────────┼───────────────┼──────────────┼─────────────────┼──────────┼────────
 view           |  1250  |          1247 |           350 |              48 | 2026...  | 2026...
 purchase       |   520  |           519 |           215 |              42 | 2026...  | 2026...
 add_to_cart    |   876  |           875 |           298 |              45 | 2026...  | 2026...
(3 rows)
```

---

## Troubleshooting

### Issue 1: "No such file or directory: config/postgres_connection_details.txt"

**Cause**: Script run from wrong directory

**Solution**:
```bash
cd Real_streaming  # Ensure you're in the project root
python src/data_generator.py
```

### Issue 2: "java.lang.ClassNotFoundException: org.postgresql.Driver"

**Cause**: PostgreSQL JDBC driver not found

**Solution**:
```bash
# Verify JAR exists
ls lib/postgresql-42.7.3.jar

# If not, download it
# Then re-run with explicit JAR path
spark-submit --driver-class-path lib/postgresql-42.7.3.jar \
              --jars lib/postgresql-42.7.3.jar \
              src/spark_streaming_to_postgres.py
```

### Issue 3: "Connection refused" from Spark job

**Cause**: PostgreSQL not running or credentials wrong

**Solution**:
```bash
# Check PostgreSQL service
psql -h localhost -U postgres -c "SELECT 1;"

# If connection fails, verify credentials
cat config/postgres_connection_details.txt

# Test connection manually
psql -h localhost -U postgres -d ecommerce_streaming
```

### Issue 4: "Permission denied" in Linux

**Cause**: File permissions not set

**Solution**:
```bash
chmod +x src/data_generator.py
chmod +x src/spark_streaming_to_postgres.py
```

### Issue 5: Spark job starts but no data appears

**Causes**: 
- Data generator not running
- CSV files not being created
- Schema mismatch

**Solution**:
```bash
# Check if CSV files exist
ls -la data/input_data/

# Check if files have correct columns
head -1 data/input_data/events_*.csv

# Check Spark UI (usually http://localhost:4040)
# Look for errors in "Completed Batches" section
```

---

## Cleanup & Reset

### Stop Services (Graceful)

**Terminal 1 & 2**: Press `Ctrl+C` in each terminal

**Terminal 3**: 
```bash
exit  # Exit PostgreSQL
```

### Clear Data for Fresh Run

```bash
# Option 1: Reset to empty table
python src/reset_spark_process.py

# Option 2: Delete CSV files
rm -rf data/input_data/*  # macOS/Linux
rmdir /s data\input_data  # Windows
mkdir data/input_data

# Option 3: Clear checkpoint
rm -rf data/checkpoint/  # macOS/Linux
rmdir /s data\checkpoint  # Windows
```

### Full Database Reset

```bash
psql -h localhost -U postgres -d ecommerce_streaming -c "TRUNCATE TABLE events;"
```

### Uninstall

```bash
# Remove Python packages
pip uninstall pyspark psycopg2-binary python-dotenv

# Note: Keep PostgreSQL and Spark for other projects
```

---

## Performance Tips

1. **Increase parallelism** for large datasets:
   ```bash
   python src/data_generator.py --max-records 500 --sleep 1
   ```

2. **Adjust Spark batch interval** if latency is high:
   - Edit `spark_streaming_to_postgres.py`
   - Change `processingTime="30 seconds"` to `"10 seconds"` for lower latency

3. **Monitor Spark UI**:
   - Open http://localhost:4040 in browser
   - Watch "Jobs" and "Stages" tabs for bottlenecks

4. **Check database performance**:
   ```sql
   -- Show slow queries
   EXPLAIN ANALYZE SELECT * FROM events WHERE user_id = 'user_1000';
   ```

---

## Next Steps

- **Testing**: See [test_cases.md](test_cases.md)
- **Metrics**: Review [performance_metrics.md](performance_metrics.md)
- **Architecture**: Study [system_architecture.txt](system_architecture.txt)
- **Walkthrough**: Follow [walkthrough.md](walkthrough.md) for detailed steps

---

**Support**: Check logs in `data_generator.log` and Spark console for errors.
