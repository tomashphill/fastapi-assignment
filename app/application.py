from logging import Logger
from typing import Callable, Dict, Optional

from fastapi import Body, FastAPI # type: ignore

from .model.database.db import *


def create_app(*, title: str, db: DB, logger: Logger) -> FastAPI:
    """
    `create_app` is a factory function to inject database and logging dependencies
    in a FastAPI application.
    """
    app = FastAPI()


    @app.get("/tag", response_model=Dict[str, int])
    async def get_tag_stats():
        """
        `get_tag_stats` will return a dictionary of name, value pairs
        for all tags currently stored in the database.
        """
        tags = await db.get_all_tags()
        logger.info("tags gathered", {"num_of_tags": len(tags)})

        # format tags to Dict[str, int]
        tags_dict = map(lambda t: t.dict(), tags)
        return {t['name']:t['value'] for t in tags_dict}


    @app.post("/tag", response_model=Tag)
    async def increment_tag(tag: TagIncrement = Body(
        ...,
        example={
            "name": "ballz",
            "value": 3
        },
    )):
        """
        `increment_tag` will increment a tag with the specified name and value.  
        If the tag does not exist, it will be created with a default value of 0,
        and incremented by the specified value.  

        Value must be a positive integer less than 10.  
        Name must be a string that conforms to [a-z_]{3,15}.  
        `TagIncrement` will take care of validation.
        """
        incremented_tag = await db.increment_tag(tag)
        logger.info(
            f"tag incremented",
            {
                "name": incremented_tag.name, 
                "value": incremented_tag.value, 
                "incrementedBy": tag.value
            }
        )
        return incremented_tag


    return app