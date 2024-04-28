from pydantic import BaseModel
from typing import List
from datetime import datetime
from .user import RoleEnum


class CommentBase(BaseModel):
    photo_id: int
    user_id: int
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    new_content: str


class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CommentDelete(BaseModel):
    comment_id: int
    user_role: RoleEnum


class CommentList(BaseModel):
    comments: List[Comment]