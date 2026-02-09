"""
Real-Time E-Commerce Data Generator
Generates CSV files with fake e-commerce events for streaming ingestion.

Usage:
    python data_generator.py [--output-dir DIR] [--min-records N] [--max-records N] [--sleep SECONDS] [--files COUNT]

Example:
    python data_generator.py --output-dir ../data/input_data --sleep 3 --files 10
"""

import argparse
import csv
import logging
import os
import random
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("data_generator.log"),
    ],
)
logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_OUTPUT_DIR = "data/input_data"
DEFAULT_MIN_RECORDS = 10
DEFAULT_MAX_RECORDS = 100
DEFAULT_SLEEP_SECONDS = 2

# Sample data
EVENT_TYPES = ["view", "purchase", "add_to_cart", "remove_from_cart"]
PRODUCT_IDS = [f"product_{i}" for i in range(1, 51)]
USER_IDS = [f"user_{i}" for i in range(1000, 1500)]


def ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist. 
    This is important for the Spark streaming job to save data files.
    output_dir = data/input_data and log file in main dir
    This is important for the Spark streaming job to monitor the directory."""
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✓ Ensured directory exists: {os.path.abspath(directory)}")
    except OSError as e:
        logger.error(f"✗ Failed to create directory: {e}")
        raise
    logger.info(f"Output directory: {os.path.abspath(directory)}")


def generate_event() -> Dict[str, str]:
    """Generate a single fake e-commerce event."""
    event_type = random.choice(EVENT_TYPES)
    is_purchase = event_type == "purchase"
    
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "product_id": random.choice(PRODUCT_IDS),
        "user_id": random.choice(USER_IDS),
        "event_timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "quantity": str(random.randint(1, 10)) if is_purchase else "0",
        "price": f"{random.uniform(5.0, 999.0):.2f}" if is_purchase else "0.00",
    }
    return event


def generate_csv_file(
    output_dir: str, file_index: int, min_records: int, max_records: int
) -> str:
    """
    Generate a CSV file with fake events.
    
    Args:
        output_dir: Directory to write CSV file default data/input_data
        file_index: Index for file naming
        min_records: Minimum records per file
        max_records: Maximum records per file
        
    Returns:
        Path to the generated CSV file
    """
    ensure_directory_exists(output_dir)
    
    timestamp = int(time.time())
    filename = f"events_{timestamp}_{file_index}.csv"
    filepath = os.path.join(output_dir, filename)

    num_records = random.randint(min_records, max_records)
    fieldnames = [
        "event_id",
        "event_type",
        "product_id",
        "user_id",
        "event_timestamp",
        "quantity",
        "price",
    ]

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for _ in range(num_records):
                writer.writerow(generate_event())
        
        logger.info(f"✓ Generated {filepath} with {num_records} records")
        return filepath
    except IOError as e:
        logger.error(f"✗ Failed to generate {filepath}: {e}")
        raise


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate fake e-commerce CSV events for streaming ingestion.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python data_generator.py
  python data_generator.py --output-dir ../data/input_data --sleep 5 --files 20
  python data_generator.py --min-records 50 --max-records 200 --sleep 2
        """,
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for CSV files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--min-records",
        type=int,
        default=DEFAULT_MIN_RECORDS,
        help=f"Minimum records per file (default: {DEFAULT_MIN_RECORDS})",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=DEFAULT_MAX_RECORDS,
        help=f"Maximum records per file (default: {DEFAULT_MAX_RECORDS})",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=DEFAULT_SLEEP_SECONDS,
        help=f"Sleep interval between files in seconds (default: {DEFAULT_SLEEP_SECONDS})",
    )
    parser.add_argument(
        "--files",
        type=int,
        default=0,
        help="Number of files to generate (0 = infinite, default: 0)",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for data generation."""
    args = parse_args()
    
    logger.info("Real-Time E-Commerce Data Generator")
    logger.info("=" * 60)
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Records per file: {args.min_records} - {args.max_records}")
    logger.info(f"Sleep interval: {args.sleep}s")
    logger.info(f"Files to generate: {'Infinite' if args.files == 0 else args.files}")
    logger.info("=" * 60)

    file_index = 0
    try:
        while True:
            generate_csv_file(
                args.output_dir, file_index, args.min_records, args.max_records
            )
            file_index += 1
            
            if args.files > 0 and file_index >= args.files:
                logger.info(f"Generated {args.files} files. Exiting.")
                break
            
            time.sleep(args.sleep)
    except KeyboardInterrupt:
        logger.warning("\nData generation stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
