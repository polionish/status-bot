import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    # Уровень логирования
    file_handler.setLevel(logging.INFO)  
    file_handler.setFormatter(logging.Formatter(log_format))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler],
    )