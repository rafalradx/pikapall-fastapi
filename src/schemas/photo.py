from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Optional


class TagIn(BaseModel):
    name: str = Field(max_length=25)


class TagOut(TagIn):
    id: int

    class Config:
        from_attributes = True


class CommentIn(BaseModel):
    content: str = Field(max_length=255)
    photo_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class CommentOut(CommentIn):
    id: int

    class Config:
        from_attributes = True


class PhotoIn(BaseModel):
    image_url: str = Field(max_length=255)
    description: str = Field(max_length=500)
    tags: List[str] | None

    @validator('tags')
    def validate_tags(cls, tags):
        if tags is not None and len(tags) > 5:
            raise ValueError("Number of tags cannot exceed 5")
        return tags


class PhotoOut(PhotoIn):
    """
    Pydantic model representing output data for retrieving a photo.

    """

    id: int
    image_url_transform: str = Field(max_length=255)
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PhotoUpdate(BaseModel):
    image_url_transform: str = Field(max_length=255)
    description: str = Field(max_length=500)
    tags: List[str] | None
