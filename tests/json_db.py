from typing import Any, Dict
from uuid import uuid1

from app.model.database.db import *


class MockDB(DB):
    def __init__(self):
        self.db: Dict[str, Dict[str, Any]]
        self.db = {}

    async def get_all_tags(self) -> List[Tag]:
        tags = [Tag.parse_obj(t) for t in self.db.values()]
        return tags

    async def increment_tag(self, tag_to_increment: TagIncrement) -> Tag:
        match = None
        for id, tag_d in self.db.items():
            if tag_d["name"] == tag_to_increment.name: # type: ignore
                self.db[id]["value"] += tag_to_increment.value
                tag = Tag.parse_obj(tag_d)
                match = True
                break

        if match is None:
            id = str(uuid1()) # generate unique id
            tag = tag_to_increment
            self.db[id] = tag_to_increment.dict()
        
        return tag


    



