import logging
import os
from config import LOG_FILE

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

_loggers: dict = {}

def get_logger(name: str) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s  %(name)-16s  %(message)s",
        datefmt="%H:%M:%S"
    )
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)   # Only warnings+ to console; file gets everything
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate = False

    _loggers[name] = logger
    return logger