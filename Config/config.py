import logging

class Config:
    # Logger Config
    LOG_FILE = "Logger/Logs/Backend.log"
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "%(asctime)s [%(funcName)s] %(levelname)s %(message)s"
    LOG_DATEFORMAT = "%d.%m.%Y %H:%M:%S"
    LOG_BACKUP_COUNT = 3
    LOG_ENCODING = "utf-8"