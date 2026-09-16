from pathlib import Path
import logging
import sys
import config

BASE_DIR=Path(__file__).resolve().parent


def setup_logger(log_level: int=config.LOG_LEVEL,log_file: Path| str=BASE_DIR / config.LOG_FILE) -> logging.Logger:
    logger = logging.getLogger(config.LOG_GET)
    logger.setLevel(log_level)
    logger.propagate = False


    if logger.handlers:
        return logger

    fmt=logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATEFMT
    )


    try:
        fh=logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except OSError as e:
        print(f"警告：日志文件 {log_file} 打不开（{e}），本次只输出到屏幕", file=sys.stderr)

    if sys.stdout is not None:
        ch=logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    return logger