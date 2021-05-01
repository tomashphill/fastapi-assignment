import re

from pydantic import BaseModel, ValidationError, validator # type: ignore


valid_name = re.compile(r"[a-z_]{3,15}", re.I)


class Tag(BaseModel):
    """
    """
    name: str
    value: int = 0


class TagIncrement(Tag):
    """
    """
    @validator('value')
    def pos_int_less_than_10(cls, v):
        if v <= 0 or v >= 10:
            raise ValueError("value must be a positive integer less than 10")
        return v

    @validator('name')
    def valid_name(cls, v):
        match = valid_name.match(v)
        if match is None:
            raise ValueError(f"{v} is not a valid string")
        return v



