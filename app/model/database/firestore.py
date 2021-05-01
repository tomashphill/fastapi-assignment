from pathlib import Path
from typing import List

from ..tag import Tag
from .db import DB

import firebase_admin # type: ignore
from firebase_admin import credentials


class FireStore(DB):
    """
    """
    def __init__(self, path_to_key: Path):
        # if not path_to_key.is_file():
        #     raise Exception(f"{path_to_key} is not a JSON file.")

        # cred = credentials.Certificate(path_to_key)
        # self.db = firebase_admin.initialize_app(cred)
        ...

    async def get_all_tags(self) -> List[Tag]:
        return [Tag()]

    async def increment_tag(self) -> Tag:
        return Tag()
    