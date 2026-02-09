import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if they already exist
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter: Use filename for clearer debugging (avoids '__main__')
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)

        # File Handler - Dynamic Naming based on component
        try:
            from pathlib import Path
            log_dir = Path("output/logs")
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Default
            filename = "project.log"
            
            # Simple routing logic - check both module name and filename
            if "ingestion" in name or "fetch_data" in name:
                filename = "ingestion.log"
            elif "processing" in name or "etl" in name:
                filename = "etl.log"
            elif "analytics" in name or "kpi" in name:
                filename = "analytics.log"
                
            log_file = log_dir / filename
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to setup file logging: {e}")
    
    return logger
