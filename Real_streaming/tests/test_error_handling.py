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

def test_connection_recovery():
    print("Manual step: Stop PostgreSQL, wait, then restart to test recovery.")
    print("Check Spark logs for recovery behavior.")

def test_malformed_csv():
    data_dir = Path(__file__).resolve().parent.parent / "data" / "input_data"
    bad_file = data_dir / "malformed_test.csv"
    with open(bad_file, "w") as f:
        f.write("bad,data,that,is,not,valid\n1,2,3,4,5,6,7,8\n")
    print(f"Malformed CSV created: {bad_file}")
    print("Check Spark logs for error handling and pipeline continuation.")

if __name__ == "__main__":
    test_connection_recovery()
    test_malformed_csv()
    print("Error handling tests completed.")
