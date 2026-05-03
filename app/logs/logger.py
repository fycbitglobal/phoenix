import os
import logging

def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("phoenix")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("logs/system.log")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()