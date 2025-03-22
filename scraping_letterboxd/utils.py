import os
import logging

def setup_logger(log_path=None):
    """Configura un logger que imprime en consola y opcionalmente guarda en archivo."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_path:
        file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def ensure_dir_exists(directory):
    os.makedirs(directory, exist_ok=True)

def log_summary(logger, total, success, failed_movies):
    logger.info(f"{total} executed, {success} success, {len(failed_movies)} errors")
    if failed_movies:
        logger.info("Failed movies:")
        for movie in failed_movies:
            logger.info(f"- {movie}")