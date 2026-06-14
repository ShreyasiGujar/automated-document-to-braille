import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name with current date
log_filename = os.path.join(
    LOG_DIR,
    f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.log"
)

# Configure logging
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

def log_results(data):
    """
    Logs OCR/Braille processing pipeline results.

    Args:
        data (dict): Dictionary containing processing details.
    """

    try:
        logging.info("===== Processing Result =====")

        for key, value in data.items():
            logging.info(f"{key}: {value}")

        logging.info("============================")

    except Exception as e:
        logging.error(f"Logging failed: {str(e)}")
