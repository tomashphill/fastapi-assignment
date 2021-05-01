from configparser import ConfigParser
from pathlib import Path
from typing import Dict

from fastapi import FastAPI # type: ignore

from app.model.database.db import DB
from app.model.database.firestore import FireStore
from app.model.tag import Tag, TagIncrement


ENV_PATH = Path(".env")
config = ConfigParser()
config.read(ENV_PATH)

# FireStore credentials
CRED = config["FireStore"]["certificate"]

app = FastAPI()
db: DB = FireStore(Path(CRED))


@app.get("/tag", response_model=Dict[str, int])
async def get_tag_stats():
    tags = await db.get_all_tags()
    tags_dict = map(lambda t: t.dict(), tags)
    return {t['name']:t['value'] for t in tags_dict}


@app.post("/tag", response_model=Tag)
async def post_tag(tag: TagIncrement):
    incremented_tag = await db.increment_tag(tag)
    return incremented_tag
