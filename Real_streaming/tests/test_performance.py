import time
import psycopg2
from pathlib import Path

def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config" / "postgres_connection_details.txt"
    config = {}
    with open(config_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                config[k.strip().lower()] = v.strip()
    return config

def test_latency():
    print("Manual step: Note CSV creation time and DB insertion time, then calculate latency.")
    print("Check pipeline logs and DB timestamps.")

def test_throughput():
    config = load_config()
    conn = psycopg2.connect(
        host=config.get("host", "localhost"),
        port=config.get("port", "5432"),
        database=config.get("database", "ecommerce_streaming"),
        user=config.get("user", "postgres"),
        password=config.get("password", "")
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM events;")
    count1 = cur.fetchone()[0]
    print(f"Initial record count: {count1}")
    print("Waiting 60 seconds to measure throughput...")
    time.sleep(60)
    cur.execute("SELECT COUNT(*) FROM events;")
    count2 = cur.fetchone()[0]
    throughput = count2 - count1
    print(f"Records inserted in 60s: {throughput}")
    print(f"Throughput: {throughput/60:.2f} records/sec")
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_latency()
    test_throughput()
    print("Performance tests completed.")
