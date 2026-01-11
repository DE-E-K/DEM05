# Manual Test Plan

| Test Case ID | Description | Steps | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-01 | Database Creation | Run `postgres_setup.sql` | Table `e_commerce_events` exists in DB | Table created successfully | Passed |
| TC-02 | CSV Generation | Run `data_generator.py` | CSV files appear in `input_data/` folder | Files generated successfully | Passed |
| TC-03 | Spark Job Start | Submit Spark job | Job starts without error, connects to DB | Job runs, connection established | Passed |
| TC-04 | Data Ingestion | Let generator run for 1 min | New rows appear in PostgreSQL table | Rows inserted correctly | Passed |
| TC-05 | Duplicate Data Handling | Stream duplicate event_ids | Duplicates filtered/rejected | Spark `dropDuplicates` added to pipeline | Passed |
| TC-06 | Authentication Recovery | Start job with incorrect password | Job fails with Auth Error | Job connects after config update | Passed |
