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

def test_data_insertion():
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
    count = cur.fetchone()[0]
    assert count > 0, "No records found in events table."
    print(f"Found {count} records in events table.")
    cur.close()
    conn.close()

def test_duplicate_handling():
    config = load_config()
    conn = psycopg2.connect(
        host=config.get("host", "localhost"),
        port=config.get("port", "5432"),
        database=config.get("database", "ecommerce_streaming"),
        user=config.get("user", "postgres"),
        password=config.get("password", "")
    )
    cur = conn.cursor()
    cur.execute("SELECT event_id, COUNT(*) FROM events GROUP BY event_id HAVING COUNT(*) > 1;")
    dups = cur.fetchall()
    assert len(dups) == 0, f"Found duplicate event_ids: {dups}"
    print("No duplicate event_ids found.")
    cur.close()
    conn.close()

def test_null_value_filtering():
    config = load_config()
    conn = psycopg2.connect(
        host=config.get("host", "localhost"),
        port=config.get("port", "5432"),
        database=config.get("database", "ecommerce_streaming"),
        user=config.get("user", "postgres"),
        password=config.get("password", "")
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM events WHERE event_id IS NULL;")
    nulls = cur.fetchone()[0]
    assert nulls == 0, f"Found {nulls} records with null event_id."
    print("No records with null event_id found.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_data_insertion()
    test_duplicate_handling()
    test_null_value_filtering()
    print("Persistence tests completed.")
