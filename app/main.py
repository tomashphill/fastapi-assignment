from configparser import ConfigParser
from pathlib import Path

from .application import create_app
from .model.database.db import DB
from .model.database.firestore import FireStore


ENV_PATH = Path(".env")
config = ConfigParser()
config.read(ENV_PATH)


def init_firestore() -> DB:
    # FireStore credentials
    CRED = config["FireStore"]["certificate"]
    return FireStore(Path(CRED))


app = create_app(title="Tagger Microservice", db=init_firestore())
