from configparser import ConfigParser
import logging
from pathlib import Path
from typing import Dict, Callable

import google.cloud.logging as glogging # type: ignore
from google.oauth2 import service_account

from .application import create_app
from .model.database.db import DB
from .model.database.firestore import FireStore


ENV_PATH = Path(".env")
config = ConfigParser()
config.read(ENV_PATH)

GOOGLE_CRED_PATH = config["Google"]["GOOGLE_APPLICATION_CREDENTIALS"]
GOOGLE_CRED = (service_account.Credentials
                              .from_service_account_file(Path(GOOGLE_CRED_PATH))
)
PROJECT_ID = config["Google"]["PROJECT_ID"]


def init_firestore() -> DB:
    """
    `init_firestore` returns an object of interface DB that will
    let the application interact with the specified FireStore database.
    """
    # FireStore credentials
    CRED = config["FireStore"]["CERTIFICATE"]
    return FireStore(Path(CRED))


def cloud_logger() -> logging.Logger:
    """
    `cloud_logger` returns a python Logger that will log to the Cloud Run project,
    formatted for structured logs.
    """
    client = glogging.Client(project=PROJECT_ID, credentials=GOOGLE_CRED)

    class CustomFormatter(logging.Formatter):
        def format(self, record):
            log_msg = super(CustomFormatter, self).format(record)
            return {
                "msg": log_msg,
                "args": record.args
            }

    handler = client.get_default_handler()
    handler.setFormatter(CustomFormatter())

    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

# create and serve
app = create_app(title="Tagger Microservice", 
                 db=init_firestore(),
                 logger=cloud_logger())
