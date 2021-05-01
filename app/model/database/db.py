from abc import ABC, abstractmethod
from typing import List

from ..tag import Tag, TagIncrement


class DB(ABC): 
    """
    `DBInterface`
    """

    @abstractmethod
    async def get_all_tags(self) -> List[Tag]:
        """
        `get_all_tags`
        """
        raise NotImplementedError

    @abstractmethod
    async def increment_tag(self, tag_to_increment: TagIncrement) -> Tag:
        raise NotImplementedError