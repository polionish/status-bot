import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Создаем обработчик для вывода в файл
    file_handler = RotatingFileHandler(
        "app.log",  # Имя файла для логов
        maxBytes=5 * 1024 * 1024,  # Максимальный размер файла (5 MB)
        backupCount=3,  # Количество резервных файлов
        encoding="utf-8"  # Кодировка
    )
    file_handler.setLevel(logging.INFO)  # Уровень логирования для файла
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler],
    )