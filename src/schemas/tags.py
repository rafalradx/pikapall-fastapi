from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int
    name: str = Field(max_length=25)
    user_id: int

    class Config:
        orm_mode = True
