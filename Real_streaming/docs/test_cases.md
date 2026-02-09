# Test Cases: Real-Time E-Commerce Streaming Pipeline

## Test Case Mapping (as of 2026-02-09)

| Test ID | Description | Script/Status |
|---------|-------------|---------------|
| TC-01 | PostgreSQL connectivity | tests/test_db_connection.py (exists) |
| TC-02 | Python dependencies | (to be created: test_python_dependencies.py) |
| TC-03 | JDBC driver availability | (to be created: test_jdbc_driver.py) |
| TC-04 | CSV file creation | (to be created: test_data_generation.py) |
| TC-05 | Data integrity (columns) | (to be created: test_data_generation.py) |
| TC-06 | Record count validation | (to be created: test_data_generation.py) |
| TC-07 | Spark job startup | (to be created: test_spark_job.py) |
| TC-08 | Schema validation | (to be created: test_spark_job.py) |
| TC-09 | File detection | (to be created: test_spark_job.py) |
| TC-10 | Data insertion | (to be created: test_persistence.py) |
| TC-11 | Duplicate handling | (to be created: test_persistence.py) |
| TC-12 | Null value filtering | (to be created: test_persistence.py) |
| TC-13 | Latency measurement | (to be created: test_performance.py) |
| TC-14 | Throughput measurement | (to be created: test_performance.py) |
| TC-15 | Connection recovery | (to be created: test_error_handling.py) |
| TC-16 | Malformed CSV handling | (to be created: test_error_handling.py) |

> Only TC-01 (DB connection) is implemented as a script. All other test scripts are missing and will be created in the next steps.

## Test Execution Summary

| Test ID | Category | Description | Status | Date | Notes |
|---------|----------|-------------|--------|------|-------|
| TC-01 | Environment | PostgreSQL connectivity | Pending | - | - |
| TC-01 | Environment | PostgreSQL connectivity | PASS | 2026-02-09 | Successfully connected to PostgreSQL |
| TC-02 | Environment | Python dependencies | Pending | - | - |
| TC-03 | Environment | JDBC driver availability | Pending | - | - |
| TC-04 | Data Generation | CSV file creation | Pending | - | - |
| TC-04 | Data Generation | CSV file creation | PASS | 2026-02-09 | 49 CSV files found, correct columns, data rows present |
| TC-05 | Data Generation | Data integrity (columns) | Pending | - | - |
| TC-05 | Data Generation | Data integrity (columns) | PASS | 2026-02-09 | All CSV files have correct columns |
| TC-06 | Data Generation | Record count validation | Pending | - | - |
| TC-06 | Data Generation | Record count validation | PASS | 2026-02-09 | All CSV files have at least 1 data row |
| TC-07 | Spark Streaming | Job startup | Pending | - | - |
| TC-07 | Spark Streaming | Job startup | FAIL | 2026-02-09 | Spark job not found: [WinError 2] The system cannot find the file specified |
| TC-08 | Spark Streaming | Schema validation | Pending | - | - |
| TC-09 | Spark Streaming | File detection | Pending | - | - |
| TC-10 | Persistence | Data insertion | Pending | - | - |
| TC-10 | Persistence | Data insertion | FAIL | 2026-02-09 | No records found in events table |
| TC-11 | Persistence | Duplicate handling | Pending | - | - |
| TC-12 | Persistence | Null value filtering | Pending | - | - |
| TC-13 | Performance | Latency measurement | Pending | - | - |
| TC-14 | Performance | Throughput measurement | Pending | - | - |
| TC-15 | Error Handling | Connection recovery | Pending | - | - |
| TC-16 | Error Handling | Malformed CSV handling | Pending | - | - |

---

## Test Case Details

### Category: Environment Setup

#### TC-01: PostgreSQL Connectivity
**Objective**: Verify PostgreSQL is accessible with configured credentials

**Prerequisites**:
- PostgreSQL installed and running
- `config/postgres_connection_details.txt` configured

**Steps**:
```bash
psql -h $(grep host config/postgres_connection_details.txt | cut -d= -f2) \
     -U $(grep user config/postgres_connection_details.txt | cut -d= -f2) \
     -d $(grep database config/postgres_connection_details.txt | cut -d= -f2) \
     -c "SELECT 1;"
```

**Expected Result**: Command returns `1` without errors

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

#### TC-02: Python Dependencies
**Objective**: Verify all required Python packages are installed

**Prerequisites**: None

**Steps**:
```bash
python -c "import pyspark; import psycopg2; import dotenv; print('All imports OK')"
```

**Expected Result**: Prints "All imports OK"

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

#### TC-03: JDBC Driver Availability
**Objective**: Verify PostgreSQL JDBC driver is available to Spark

**Prerequisites**: PostgreSQL JDBC driver downloaded

**Steps**:
```bash
ls -la lib/postgresql-42.7.3.jar
```

**Expected Result**: File exists and is > 500KB

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

### Category: Data Generation

#### TC-04: CSV File Creation
**Objective**: Verify data generator creates CSV files in correct location

**Prerequisites**: Data generator script in place

**Steps**:
```bash
# Clear previous files
rm -rf data/input_data/*

# Run generator for 10 seconds
timeout 10 python src/data_generator.py --files 3 2>/dev/null || true

# Check files created
ls -la data/input_data/
```

**Expected Result**: At least 2-3 CSV files appear in `data/input_data/`

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

**Evidence**: (example)
```
events_1707370245_0.csv  (47 records)
events_1707370248_1.csv  (52 records)
events_1707370251_2.csv  (38 records)
```

---

#### TC-05: CSV Data Integrity
**Objective**: Verify generated CSV files have correct columns

**Prerequisites**: CSV files generated (TC-04 passed)

**Steps**:
```bash
# Check header row
head -1 data/input_data/events_*.csv
```

**Expected Result**: Header contains: `event_id,event_type,product_id,user_id,event_timestamp,quantity,price`

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

#### TC-06: Record Count Validation
**Objective**: Verify CSV files contain expected number of records

**Prerequisites**: CSV files generated (TC-04 passed)

**Steps**:
```bash
# Count records in first CSV (excluding header)
wc -l data/input_data/events_*.csv | head -1
```

**Expected Result**: Row count between 11-101 (10-100 records + 1 header)

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

### Category: Spark Streaming

#### TC-07: Spark Job Startup
**Objective**: Verify Spark streaming job starts without errors

**Prerequisites**:
- TC-01 passes (PostgreSQL accessible)
- TC-03 passes (JDBC driver available)

**Steps**:
```bash
# Start generator in background
python src/data_generator.py --files 5 &
GEN_PID=$!

# Start Spark job with short timeout
timeout 30 spark-submit --driver-class-path lib/postgresql-42.7.3.jar \
    --jars lib/postgresql-42.7.3.jar \
    src/spark_streaming_to_postgres.py 2>&1 | grep -E "(Streaming query|ERROR)" &
SPARK_PID=$!

sleep 15
kill $SPARK_PID 2>/dev/null || true
kill $GEN_PID 2>/dev/null || true
```

**Expected Result**: 
- Spark job starts without Java/ClassNotFoundException
- Message shows "Streaming query started"
- No permission or connection errors

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

#### TC-08: Schema Validation
**Objective**: Verify Spark validates CSV schema correctly

**Prerequisites**: CSV files exist (TC-04 passed)

**Steps**:
1. Create a malformed CSV in `data/input_data/bad_data.csv`:
```csv
event_id,event_type,product_id
uuid1,view,p1
```

2. Monitor Spark logs for schema errors

**Expected Result**: Spark logs show schema mismatch error or skips malformed file

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

#### TC-09: Automatic File Detection
**Objective**: Verify Spark detects new CSV files automatically

**Prerequisites**: 
- Spark job running for at least 30 seconds
- Initial CSV files exist

**Steps**:
1. Monitor `data/input_data/` for new files
2. Generate a new CSV file:
```bash
python -c "
import csv, uuid, random, time
with open('data/input_data/test_' + str(int(time.time())) + '.csv', 'w') as f:
    w = csv.DictWriter(f, ['event_id','event_type','product_id','user_id','event_timestamp','quantity','price'])
    w.writeheader()
    w.writerow({'event_id': str(uuid.uuid4()), 'event_type': 'view', 'product_id': 'p1', 'user_id': 'u1', 'event_timestamp': '2026-02-08 10:30:45', 'quantity': '0', 'price': '0.00'})
"
```

3. Check Spark logs for "Writing batch" message

**Expected Result**: Spark detects and processes the new file within 30 seconds

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

### Category: Data Persistence

#### TC-10: Data Insertion into PostgreSQL
**Objective**: Verify data is correctly inserted into PostgreSQL

**Prerequisites**:
- Data generator running
- Spark job running for > 1 minute

**Steps**:
```bash
# Count records in database
psql -h localhost -U postgres -d ecommerce_streaming -c "SELECT COUNT(*) FROM events;"
```

**Expected Result**: 
- Count > 0 (typically 50-500 depending on generators)
- Number increases each time command is run

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

**Evidence**: (example)
```
First check:  42 records
After 1 min: 156 records
After 2 min: 289 records
```

---

#### TC-11: Duplicate Prevention
**Objective**: Verify duplicate event_ids are not inserted

**Prerequisites**: TC-10 passed (data in database)

**Steps**:
```bash
# Check for duplicates
psql -h localhost -U postgres -d ecommerce_streaming -c "
SELECT event_id, COUNT(*) as cnt FROM events 
GROUP BY event_id HAVING COUNT(*) > 1;
"
```

**Expected Result**: Returns empty result set (no duplicates)

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

#### TC-12: Null Value Filtering
**Objective**: Verify records with null event_id are filtered out

**Prerequisites**: TC-10 passed

**Steps**:
```bash
# Check for null event_ids in database
psql -h localhost -U postgres -d ecommerce_streaming -c "
SELECT COUNT(*) FROM events WHERE event_id IS NULL;
"
```

**Expected Result**: Returns 0

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

### Category: Performance

#### TC-13: Latency Measurement
**Objective**: Measure time from CSV creation to database insertion

**Prerequisites**: 
- Data generator running
- Spark job running
- Tools: `stat` command or file timestamp utilities

**Steps**:
```bash
# 1. Note current database record count
psql -h localhost -U postgres -d ecommerce_streaming -c "SELECT COUNT(*) FROM events;" > /tmp/before.txt

# 2. Generate a new CSV file
python src/data_generator.py --files 1

# 3. Record the CSV creation time (using file timestamp)
ls -la data/input_data/ | tail -1

# 4. Poll database for new records
sleep 5
psql -h localhost -U postgres -d ecommerce_streaming -c "SELECT COUNT(*) FROM events;" > /tmp/after.txt

# 5. Calculate difference
BEFORE=$(cat /tmp/before.txt | tail -1)
AFTER=$(cat /tmp/after.txt | tail -1)
DIFF=$((AFTER - BEFORE))
echo "Inserted $DIFF records"
```

**Expected Result**: 
- New records appear within 30-60 seconds
- Latency < 1 minute for typical configurations

**Actual Result**: [TO BE FILLED]

**Evidence**: (example)
```
CSV created:  10:30:45
Batch inserted: 10:31:02
Latency: ~17 seconds
```

---

#### TC-14: Throughput Measurement
**Objective**: Measure records processed per second

**Prerequisites**: Pipeline running for at least 5 minutes

**Steps**:
```bash
# Run for 5 minutes with known parameters
time_start=$(date +%s)
echo "Pipeline running... (5 minutes)"
sleep 300
time_end=$(date +%s)

# Get event count
record_count=$(psql -h localhost -U postgres -d ecommerce_streaming -c "SELECT COUNT(*) FROM events;" | tail -2 | head -1 | xargs)

# Calculate throughput
duration=$((time_end - time_start))
throughput=$(echo "scale=2; $record_count / $duration" | bc)

echo "Generated $record_count records in $duration seconds"
echo "Throughput: $throughput records/second"
```

**Expected Result**: 
- Throughput: 10-50 records/second (depending on configuration)
- System remains stable

**Actual Result**: [TO BE FILLED]

**Evidence**: (example)
```
Generated 2847 records in 300 seconds
Throughput: 9.49 records/second
```

---

### Category: Error Handling

#### TC-15: Database Connection Recovery
**Objective**: Verify pipeline handles temporary connection loss

**Prerequisites**: Pipeline running normally

**Steps**:
1. Note the time and record count
2. Stop PostgreSQL service
3. Wait 60 seconds
4. Restart PostgreSQL
5. Check if pipeline recovers and resumes writing

**Expected Result**:
- Error messages appear in Spark logs
- After PostgreSQL restarts, pipeline resumes writing
- No data loss (batch retried from checkpoint)

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

#### TC-16: Malformed CSV Handling
**Objective**: Verify pipeline handles corrupt CSV files gracefully

**Prerequisites**: Pipeline running

**Steps**:
1. Create a corrupted CSV file:
```bash
echo "corrupt data that is not valid csv format" > data/input_data/corrupt.csv
```

2. Monitor Spark logs for errors
3. Verify pipeline continues processing other files

**Expected Result**:
- Spark logs show parsing error for corrupt file
- Pipeline continues processing (doesn't crash)
- Other CSV files are still processed

**Actual Result**: [TO BE FILLED]

**Pass/Fail**: ☐ PASS ☐ FAIL

---

## Test Execution Notes

### How to Run All Tests

```bash
# 1. Prepare environment
cd Real_streaming

# 2. Run environment setup tests (TC-01 to TC-03)
bash test_environment.sh  # (if script provided)

# 3. Generate data for testing
python src/data_generator.py --files 10 &
GEN_PID=$!

# 4. Start Spark job
spark-submit --driver-class-path lib/postgresql-42.7.3.jar \
             --jars lib/postgresql-42.7.3.jar \
             src/spark_streaming_to_postgres.py &
SPARK_PID=$!

# 5. Run functional tests (TC-04 to TC-16)
bash test_functional.sh  # (if script provided)

# 6. Cleanup
kill $GEN_PID $SPARK_PID
```

### Pass Criteria

**Overall Test Pass**: ≥ 14/16 tests pass

**Critical Tests** (must pass):
- TC-01: PostgreSQL connectivity
- TC-04: CSV file creation
- TC-07: Spark job startup
- TC-10: Data insertion

---

## Test Results Summary

**Test Execution Date**: [TO BE FILLED]

**Executed By**: [TO BE FILLED]

**Overall Result**: ☐ PASS ☐ FAIL

**Pass Rate**: ____ / 16 tests passed

**Comments**: 

[TO BE FILLED]

---

**Next Steps**: If all tests pass, proceed with Performance Metrics (performance_metrics.md)
