from abc import ABC, abstractmethod
from typing import List

from ..tag import Tag


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
    async def increment_tag(self) -> Tag:
        raise NotImplementedError