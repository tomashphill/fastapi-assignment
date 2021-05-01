from pathlib import Path

from fastapi import FastAPI # type: ignore

from app.model.database.firestore import FireStore
from app.model.database.db import DB


CREDENTIALS = "../static/credentials"

app = FastAPI()
db: DB = FireStore(Path(CREDENTIALS))


@app.get("/tag")
async def get_tags():
    return db.get_all_tags()

@app.post("/tag")
async def post_tag():
    return "goodbye"
