from abc import ABC, abstractmethod
from typing import List

from ..tag import Tag, TagIncrement


class DB(ABC): 
    """
    The application will use the interface `DB` in order to interact
    with whatever database is conretely implemented.
    """

    @abstractmethod
    async def get_all_tags(self) -> List[Tag]:
        raise NotImplementedError

    @abstractmethod
    async def increment_tag(self, tag_to_increment: TagIncrement) -> Tag:
        raise NotImplementedError