import logging
from config.settings import LOG_PATH

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        foomatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        fh = logging.FileHandler(LOG_PATH, encoding='utf-8')
        fh.setFormatter(foomatter)
        logger.addHandler(fh)
    
    return logger