import os
import glob
import csv
from pathlib import Path

def test_csv_file_creation():
    """Test that CSV files are created in the data/input_data directory."""
    data_dir = Path(__file__).resolve().parent.parent / "data" / "input_data"
    files = list(data_dir.glob("events_*.csv"))
    assert len(files) > 0, f"No CSV files found in {data_dir}"
    print(f"Found {len(files)} CSV files in {data_dir}")
    return files

def test_csv_columns(files):
    """Test that CSV files have correct columns."""
    expected = ["event_id","event_type","product_id","user_id","event_timestamp","quantity","price"]
    for f in files:
        with open(f, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            assert header == expected, f"File {f} has incorrect columns: {header}"
    print("All CSV files have correct columns.")

def test_csv_record_count(files):
    """Test that CSV files have at least 1 data row (excluding header)."""
    for f in files:
        with open(f, newline='', encoding='utf-8') as csvfile:
            row_count = sum(1 for _ in csvfile) - 1
            assert row_count > 0, f"File {f} has no data rows."
    print("All CSV files have at least 1 data row.")

if __name__ == "__main__":
    files = test_csv_file_creation()
    test_csv_columns(files)
    test_csv_record_count(files)
    print("Data generation tests passed.")
