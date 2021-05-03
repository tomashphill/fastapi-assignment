import os
from pathlib import Path
from typing import List

import firebase_admin # type: ignore
from firebase_admin import credentials
from firebase_admin import firestore

from ..tag import Tag
from .db import DB


class FireStore(DB):
    """
    `FireStore` is a concrete definition of the DB interface.
    A path to the JSON credentials must me supplied.
    """
    def __init__(self, cred_path: Path):
        if not cred_path.is_file():
            raise Exception(f"{cred_path} is not a file.")

        cred = credentials.Certificate(cred_path)
        app = firebase_admin.initialize_app(cred)

        self.db: firestore.firestore.Client # declared for mypy
        self.db = firestore.client(app)

    async def get_all_tags(self) -> List[Tag]:
        tags = self.db.collection(u'tags').stream()
        return [Tag.parse_obj(t.to_dict()) for t in tags]
    
    async def increment_tag(self, tag_to_increment: Tag) -> Tag:
        """
        `increment_tag` will increment the tag `tag_to_increment.name` 
        by `tag_to_increment.value`. If the tag doesn't exist, a new one
        will be created and stored in the database with value `tag_to_increment.value`.
        """
        possible_tag = (self.db.collection(u'tags')
                .where(u'name', u'==', tag_to_increment.name)
                .limit(1)
                .stream())
        possible_tag = list(possible_tag)

        if possible_tag:
            id = possible_tag[0].id
            tag = Tag.parse_obj(possible_tag[0].to_dict())
            tag.value += tag_to_increment.value
            self.db.collection(u'tags').document(id).set(tag.dict())
        else:
            tag = tag_to_increment
            self.db.collection(u'tags').add(tag.dict())

        return tag

        

       
    