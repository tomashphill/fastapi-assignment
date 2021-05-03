from pydantic import BaseModel, constr, conint


class Tag(BaseModel):
    name: str
    value: int

class TagIncrement(Tag):
    name: constr(regex=r"[a-z_]{3,15}") # type: ignore
    value: conint(gt=0, lt=10) # type: ignore



