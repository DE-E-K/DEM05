
import psycopg2
import os
from pathlib import Path

def load_config(config_file):
    config = {}
    with open(config_file, "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip().lower()] = value.strip()
    return config

def test_connection():
    try:
        # Resolve config path relative to this script
        # Assumes script is in tests/, config is in ../config/
        base_dir = Path(__file__).resolve().parent.parent
        config_path = base_dir / "config" / "postgres_connection_details.txt"
        
        print(f"Loading config from: {config_path}")
        if not config_path.exists():
            print("Config file not found!")
            return

        config = load_config(config_path)
        
        print("Attempting to connect with:")
        print(f"Host: {config.get('host')}")
        print(f"Port: {config.get('port')}")
        print(f"DB: {config.get('database')}")
        print(f"User: {config.get('user')}")
        
        conn = psycopg2.connect(
            host=config.get("host", "localhost"),
            port=config.get("port", "5432"),
            database=config.get("database", "ecommerce_streaming"),
            user=config.get("user", "postgres"),
            password=config.get("password", "")
        )
        print("Successfully connected to PostgreSQL!")
        conn.close()
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    test_connection()
