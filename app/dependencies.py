from configparser import ConfigParser
import logging
from pathlib import Path
import sys

from fastapi import Depends
from pythonjsonlogger import jsonlogger

from .model.database.db import DB
from .model.database.firestore import FireStore


ENV_PATH = Path(".env")
config = ConfigParser()
config.read(ENV_PATH)

    #########################
    #  DATABASE DEPENDENCY  #
    #########################

def get_db() -> DB:
    return firestore_db

FIRESTORE_CRED = config["FireStore"]["CERTIFICATE"]
firestore_db = FireStore(Path(FIRESTORE_CRED))

    ########################
    #  LOGGING DEPENDENCY  #    
    ########################      

# should logging be a dependency if we ca just use "logging.get_logger()"?
def get_logger() -> logging.Logger:
    return app_logger

logging.basicConfig(level=logging.DEBUG)

class StackDriverJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, fmt="%(levelname) %(message) %(asctime)", style="%", *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record["severity"] = log_record['levelname']
        log_record
        del log_record["levelname"]
        return super(StackDriverJsonFormatter, self).process_log_record(log_record)

handler = logging.StreamHandler(sys.stdout)
formatter = StackDriverJsonFormatter()
handler.setFormatter(formatter)

app_logger = logging.getLogger()
app_logger.addHandler(handler)


