from datetime import datetime
from pydantic import BaseModel, Field


class TagIn(BaseModel):
    name: str = Field(max_length=25)


class TagOut(TagIn):
    id: int

    class Config:
        from_attributes = True
