import csv
import time
import os
import random
import uuid
from datetime import datetime

# Configuration
INPUT_DATA_DIR = 'input_data'
MIN_RECORDS = 1
MAX_RECORDS = 50
SLEEP_INTERVAL = random.randint(1, 10)  # Seconds between file creation

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_event():
    event_types = ['view', 'purchase', 'add_to_cart', 'click']
    product_ids = [f'PROD-{random.randint(1, 100):03d}' for _ in range(100)]
    user_ids = [f'USER-{random.randint(1, 1000):04d}' for _ in range(1000)]
    
    event_type = random.choice(event_types)
    price = round(random.uniform(10.0, 500.0), 2) if event_type == 'purchase' else None
    quantity = random.randint(1, 5) if event_type == 'purchase' else None

    return {
        'event_id': str(uuid.uuid4()),
        'event_type': event_type,
        'product_id': random.choice(product_ids),
        'user_id': random.choice(user_ids),
        'event_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'quantity': quantity,
        'price': price
    }

def generate_csv_file(file_index):
    ensure_directory_exists(INPUT_DATA_DIR)
    filename = f"events_{int(time.time())}_{file_index}.csv"
    filepath = os.path.join(INPUT_DATA_DIR, filename)

    num_records = random.randint(MIN_RECORDS, MAX_RECORDS)

    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['event_id', 'event_type', 'product_id', 'user_id', 'event_timestamp', 'quantity', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for _ in range(num_records):
            writer.writerow(generate_event())
    
    print(f"Generated {filepath} with {num_records} records.")

def main():
    print("Starting data generator...")
    file_index = 0
    try:
        while True:
            generate_csv_file(file_index)
            file_index += 1
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print("\nData generation stopped.")

if __name__ == "__main__":
    main()
