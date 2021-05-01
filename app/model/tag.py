from pydantic import BaseModel

class Tag(BaseModel):
    id: int
    tag: str
    value: int = 0