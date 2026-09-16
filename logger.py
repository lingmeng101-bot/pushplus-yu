from pathlib import Path
import logging
import config

BASE_DIR=Path(__file__).resolve().parent

def setup_logger(log_level: int=config.LOG_LEVEL,log_file: Path| str=BASE_DIR / config.LOG_FILE) -> logging.Logger:
    logger = logging.getLogger(config.LOG_GET)
    logger.setLevel(log_level)

    if any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        return logger

    fmt=logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATEFMT
    )
    fh=logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    logger.propagate = False
    return logger

