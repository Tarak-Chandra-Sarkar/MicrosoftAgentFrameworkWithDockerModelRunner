import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.getenv("LOG_FILE", "Agent.log")

# Ensure directory exists
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

LOG_FORMAT = "%(asctime)s [%(levelname)s] (%(name)s) %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str) -> logging.Logger:
    """Configures and returns a logger that logs to console and file."""
    logger = logging.getLogger(name)

    if not logger.handlers:  # avoid duplicates
        logger.setLevel(logging.DEBUG)

        # # Console handler
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Formatters
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        # console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers
        # logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
