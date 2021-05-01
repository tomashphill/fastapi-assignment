from typing import Dict

from fastapi import FastAPI # type: ignore

from .model.database.db import *


def create_app(*, title: str, db: DB) -> FastAPI:
    app = FastAPI()

    @app.get("/tag", response_model=Dict[str, int])
    async def get_tag_stats():
        tags = await db.get_all_tags()
        tags_dict = map(lambda t: t.dict(), tags)
        return {t['name']:t['value'] for t in tags_dict}

    @app.post("/tag", response_model=Tag)
    async def post_tag(tag: TagIncrement):
        incremented_tag = await db.increment_tag(tag)
        return incremented_tag

    return app