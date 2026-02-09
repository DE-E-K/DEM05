# Walkthrough: Building and Running the Real-Time Streaming Pipeline

This is a **step-by-step walkthrough** for someone building or deploying this project for the first time.

---

## Part 1: Environment Verification (5 minutes)

### Step 1.1: Test Python Installation

```bash
python --version
# Output: Python 3.8.x or higher

python -c "import sys; print(sys.executable)"
# Shows your Python executable path
```

### Step 1.2: Test Java Installation

```bash
java -version
# Output: java version "11.x.x" or higher

# Locate Java (for Spark configuration)
where java  # Windows
which java  # macOS/Linux
```

### Step 1.3: Test PostgreSQL

```bash
psql --version
# Output: psql (PostgreSQL) 12.x or higher

# Check if PostgreSQL service is running
psql -U postgres -c "SELECT version();"
# Should show PostgreSQL version if running
```

**Troubleshoot**: If any command fails, go back to [user_guide.md → Prerequisites](user_guide.md#prerequisites)

---

## Part 2: Project Setup (10 minutes)

### Step 2.1: Navigate to Project Directory

```bash
cd "c:\Users\Amalitech\OneDrive - AmaliTech gGmbH\Desktop\Moodle Labs\Specilization\DEM05\Real_streaming"

# Verify structure
ls -la  # macOS/Linux
dir     # Windows
```

**Expected output**:
```
src/
data/
config/
docs/
lib/
tests/
README.md
```

### Step 2.2: Install Python Dependencies

```bash
pip install -r src/requirements.txt

# Verify installation
python -c "import pyspark; import psycopg2; print('✓ Dependencies OK')"
```

### Step 2.3: Verify PostgreSQL JDBC Driver

```bash
ls lib/postgresql-42.7.3.jar  # macOS/Linux
dir lib\postgresql-42.7.3.jar  # Windows

# File size should be ~800KB+
```

If missing:
```bash
# Download from: https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
# Place in lib/ directory
```

---

## Part 3: Database Setup (10 minutes)

### Step 3.1: Connect to PostgreSQL

```bash
psql -h localhost -U postgres
```

You should see the `postgres=#` prompt.

### Step 3.2: Create Database and Table

```sql
\i config/postgres_setup.sql
```

**Expected output**:
```
CREATE DATABASE
CREATE TABLE
CREATE INDEX (x4)
GRANT (x3)
 tablename
────────────
 events
(1 row)
```

### Step 3.3: Verify Table Creation

```sql
\c ecommerce_streaming

\dt
-- Should show: events | table | postgres

SELECT * FROM events;
-- Should return empty result (0 rows)

\q  -- Exit PostgreSQL
```

### Step 3.4: Verify Database Credentials

Check `config/postgres_connection_details.txt`:

```bash
cat config/postgres_connection_details.txt  # macOS/Linux
type config\postgres_connection_details.txt  # Windows
```

**Expected output**:
```
host=localhost
port=5432
database=ecommerce_streaming
user=postgres
password=LearnStreaming!2026
table=events
```

If your password is different, edit the file:

```bash
# Edit in your text editor
notepad config\postgres_connection_details.txt  # Windows
nano config/postgres_connection_details.txt     # macOS/Linux
```

---

## Part 4: Running the Pipeline (30 minutes total)

This part requires three terminal windows. Follow the exact sequence.

### Step 4.1: Open Terminal 1 - Data Generator

```bash
# Navigate to project root
cd "c:\Users\Amalitech\OneDrive - AmaliTech gGmbH\Desktop\Moodle Labs\Specilization\DEM05\Real_streaming"

# Start generator (creates CSV files)
python src/data_generator.py
```

**Expected output**:
```
============================================================
Real-Time E-Commerce Data Generator
============================================================
Output directory: C:\...\Real_streaming\data\input_data
Records per file: 10 - 100
Sleep interval: 2s
Files to generate: Infinite
============================================================
✓ Generated C:\...\events_1707370245_0.csv with 47 records
✓ Generated C:\...\events_1707370248_1.csv with 52 records
✓ Generated C:\...\events_1707370251_2.csv with 38 records
...
```

✅ **Keep this terminal running. Do not close it.**

---

### Step 4.2: Open Terminal 2 - Spark Streaming Job

**In a new terminal window**:

```bash
cd "c:\Users\Amalitech\OneDrive - AmaliTech gGmbH\Desktop\Moodle Labs\Specilization\DEM05\Real_streaming"

spark-submit --driver-class-path lib/postgresql-42.7.3.jar \
              --jars lib/postgresql-42.7.3.jar \
              src/spark_streaming_to_postgres.py
```

**Expected output** (after 10-15 seconds):
```
============================================================
Real-Time E-Commerce Streaming Pipeline
============================================================
Monitoring directory: C:\...\Real_streaming\data\input_data
Database: ecommerce_streaming
Table: events
============================================================
INFO Streaming query started. Waiting for termination...
Batch 0: Writing 47 records to events...
Batch 0: Successfully wrote 47 records.
Batch 1: Writing 52 records to events...
Batch 1: Successfully wrote 52 records.
...
```

✅ **Keep this terminal running. Do not close it.**

---

### Step 4.3: Open Terminal 3 - Verify Data Flow

**In a third terminal window**:

```bash
# Navigate to project
cd "c:\Users\Amalitech\OneDrive - AmaliTech gGmbH\Desktop\Moodle Labs\Specilization\DEM05\Real_streaming"

# Connect to PostgreSQL
psql -h localhost -U postgres -d ecommerce_streaming
```

**Now you're in PostgreSQL. Run verification queries**:

#### Query 1: Check total records (run every 10 seconds)

```sql
SELECT COUNT(*) as total_records FROM events;
```

**Expected**: Number increases (e.g., 47 → 99 → 151 → ...)

#### Query 2: View latest events

```sql
SELECT 
    event_id, 
    event_type, 
    user_id, 
    event_timestamp 
FROM events 
ORDER BY event_timestamp DESC 
LIMIT 5;
```

**Expected**: 5 most recent events with all columns populated

#### Query 3: Breakdown by event type

```sql
SELECT event_type, COUNT(*) FROM events GROUP BY event_type;
```

**Expected output** (example after 1 minute):
```
  event_type   | count
──────────────┼──────
 view         |   45
 purchase     |   28
 add_to_cart  |   32
(3 rows)
```

#### Query 4: Check for duplicates (should be 0)

```sql
SELECT event_type, COUNT(*) as cnt FROM events 
GROUP BY event_id HAVING COUNT(*) > 1;
```

**Expected**: Empty result (0 rows) = no duplicates ✓

---

## Part 5: Monitoring the Pipeline (Continuous)

### Terminal 3 Monitoring Loop

Run this in Terminal 3 to continuously monitor:

```sql
-- Run every 10-15 seconds
SELECT 
    COUNT(*) as total,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT product_id) as unique_products,
    MAX(event_timestamp) as latest_event
FROM events;
```

### Spark Monitoring

Open a web browser:

```
http://localhost:4040
```

Navigate to:
- **Jobs**: See completed and running jobs
- **Stages**: View stage execution times
- **Executors**: Monitor memory and CPU
- **Streaming**: View batch statistics

---

## Part 6: Manual Testing (Optional, 10 minutes)

### Test 1: Generate events faster

Stop the current generator (Ctrl+C in Terminal 1), then:

```bash
# Faster generation: 5 files with higher volume
python src/data_generator.py --min-records 100 --max-records 500 --sleep 1 --files 5
```

Observe:
- More records per file
- Faster file generation
- Database record count increases faster

### Test 2: Create a malformed CSV

In Terminal 3:

```bash
# Exit PostgreSQL first
\q
```

Then create a bad file:

```bash
# Create malformed CSV
echo "bad,data,that,is,not,valid" > data/input_data/test_bad.csv
```

Check Spark logs in Terminal 2. You should see a parsing error, but the pipeline continues processing other files.

### Test 3: Check data quality

In Terminal 3:

```bash
psql -h localhost -U postgres -d ecommerce_streaming

-- Check for null values
SELECT COUNT(*) FROM events WHERE event_id IS NULL;
-- Should be 0

-- Check price values
SELECT 
    event_type,
    COUNT(*) as count,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM events 
WHERE price > 0
GROUP BY event_type;
```

---

## Part 7: Cleanup & Shutdown (5 minutes)

### Stop the Pipeline

**In Terminal 1**: Press `Ctrl+C`
```
Data generation stopped by user.
```

**In Terminal 2**: Press `Ctrl+C`
```
Stopping Spark job...
```

**In Terminal 3**:
```bash
exit  # or \q
```

### Clear Data for Fresh Run (Optional)

```bash
# Option 1: Reset database table
python src/reset_spark_process.py

# Option 2: Delete CSV files
rm -rf data/input_data/*  # macOS/Linux
rmdir /s data\input_data  # Windows (then mkdir data\input_data)
```

### Verify Shutdown

```bash
# Check no Java processes running
jps  # or: tasklist | grep java (Windows)

# Check Spark UI is inaccessible
# Try opening http://localhost:4040 (should fail)
```

---

## Troubleshooting Guide

### Issue: "No such file or directory: config/postgres_connection_details.txt"

**Cause**: Running from wrong directory

**Fix**:
```bash
pwd  # Check current directory
# Should end with: Real_streaming

cd "../Real_streaming"  # Navigate to project root
python src/data_generator.py
```

### Issue: Spark job doesn't start - "ClassNotFoundException: org.postgresql.Driver"

**Cause**: JDBC driver not found

**Fix**:
```bash
ls lib/postgresql-42.7.3.jar  # Check file exists

# If missing, download and place in lib/
# Then retry with explicit path
spark-submit --driver-class-path lib/postgresql-42.7.3.jar \
             --jars lib/postgresql-42.7.3.jar \
             src/spark_streaming_to_postgres.py
```

### Issue: "Connection refused" - can't connect to PostgreSQL

**Cause**: PostgreSQL not running or wrong credentials

**Fix**:
```bash
# Check PostgreSQL service
psql -h localhost -U postgres -c "SELECT 1;"
# If fails, start PostgreSQL service

# Verify credentials in config file
cat config/postgres_connection_details.txt
# Update password if needed
```

### Issue: No data appearing in database

**Cause**: Could be several things

**Debug steps**:
```bash
# 1. Check CSV files exist
ls data/input_data/

# 2. Check CSV file format
head -2 data/input_data/events_*.csv
# Should show header + data rows

# 3. Check Spark logs for errors
# Look for "ERROR" in Terminal 2 output

# 4. Check database table
psql -c "SELECT COUNT(*) FROM events;"
```

---

## Next Steps After Successful Run

1. **Read** [project_overview.md](project_overview.md) - Understand architecture
2. **Review** [test_cases.md](test_cases.md) - Run full test suite
3. **Check** [performance_metrics.md](performance_metrics.md) - Understand the numbers
4. **Study** [system_architecture.txt](system_architecture.txt) - Deep dive

---

## Time Breakdown

| Step | Component | Time |
|------|-----------|------|
| Part 1 | Verify environment | 5 min |
| Part 2 | Project setup | 10 min |
| Part 3 | Database setup | 10 min |
| Part 4 | Run pipeline | 30 min |
| Part 5 | Monitor | 10 min |
| Part 6 | Manual testing | 10 min |
| Part 7 | Shutdown | 5 min |
| **Total** | | **80 minutes** |

---

## Success Criteria

✅ All three terminals running without errors
✅ CSV files generating in data/input_data/
✅ Spark logs showing "Writing batch X to PostgreSQL..."
✅ Database record count increasing every ~30 seconds
✅ SELECT COUNT(*) shows > 100 records in events table

---

**Happy streaming! 🚀**
