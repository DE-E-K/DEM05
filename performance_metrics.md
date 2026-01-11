# Performance Metrics Report

**System Logic/Throughput Recording**

| Metric | Description | Value / Observation | Measurement Method |
| :--- | :--- | :--- | :--- |
| **Input Rate** | Events generated per second | ~0.2 - 3 events/sec | `MAX_RECORDS` (50) / `SLEEP_INTERVAL` (avg 4.5s) |
| **Processing Rate** | Rows processed per second by Spark | Varies | Check Spark UI or Console Logs |
| **Latency** | Time from CSV creation to DB insertion | < 10 seconds | Compare `event_timestamp` vs DB insertion time |
| **Throughput** | Total records processed in 5 min run | ~2000-30000 records | `SELECT COUNT(*) FROM e_commerce_events;` |
| **Error Rate** | Percentage of failed batches/records | 0% | Check logs for exceptions |

## Observations
*Record any observations about system stability, memory usage, or bottlenecks here.*
