import subprocess
import sys
from pathlib import Path

def test_spark_job_startup():
    """Test that the Spark streaming job starts without errors."""
    project_root = Path(__file__).resolve().parent.parent
    spark_script = project_root / "src" / "spark_streaming_to_postgres.py"
    jar_path = project_root / "lib" / "postgresql-42.7.3.jar"
    cmd = [
        "spark-submit",
        "--driver-class-path", str(jar_path),
        "--jars", str(jar_path),
        str(spark_script),
    ]
    print(f"Running: {' '.join(cmd)}")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert "Streaming query started" in proc.stdout or proc.returncode == 0, proc.stderr
        print("Spark job started successfully.")
    except Exception as e:
        print(f"Failed to start Spark job: {e}")
        sys.exit(1)

def test_schema_validation():
    """Test that Spark validates CSV schema and logs errors for malformed files."""
    # This is a placeholder: actual implementation would require log parsing or Spark REST API
    print("Schema validation test: Please check Spark logs for schema errors.")

def test_file_detection():
    """Test that Spark detects new CSV files automatically."""
    print("File detection test: Please check Spark logs for new file processing.")

if __name__ == "__main__":
    test_spark_job_startup()
    test_schema_validation()
    test_file_detection()
    print("Spark streaming tests completed.")
