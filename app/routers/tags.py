from logging import Logger
from typing import Dict

from fastapi import APIRouter, Body, Depends

from ..dependencies import get_db, get_logger
from ..model.database.db import *


router = APIRouter(
    prefix="/tag",
    tags=["tag"],
)

@router.get("", response_model=Dict[str, int])
async def get_tag_stats(db: DB = Depends(get_db), 
                        logger: Logger = Depends(get_logger)):
    """
    `get_tag_stats` will return a dictionary of name, value pairs
    for all tags currently stored in the database.
    """
    tags = await db.get_all_tags()
    logger.info("tags gathered", extra={"num_of_tags": len(tags)})

    # format tags to Dict[str, int]
    tags_dict = map(lambda t: t.dict(), tags)
    return {t['name']:t['value'] for t in tags_dict}


@router.post("", response_model=Tag)
async def increment_tag(tag: TagIncrement = Body(
    ...,
    example={
        "name": "ballz",
        "value": 3
    },
), db: DB = Depends(get_db), logger: Logger = Depends(get_logger)):
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
        extra={
            "name": incremented_tag.name, 
            "value": incremented_tag.value, 
            "incrementedBy": tag.value
        }
    )
    return incremented_tag