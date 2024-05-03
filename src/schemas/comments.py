from pydantic import BaseModel, Field
from datetime import datetime


class CommentIn(BaseModel):
    photo_id: int
    content: str = Field(max_length=255)


class CommentUpdate(BaseModel):
    content: str


class CommentOut(CommentIn):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
