from datetime import datetime
from pydantic import BaseModel, Field
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
    """
    Pydantic model representing input data for creating a photo.

    """

    image_url: str = Field(max_length=255)
    description: str = Field(max_length=500)
    tags: List[int] | None


class PhotoOut(PhotoIn):

    id: int
    image_url_transform: str = Field(max_length=255)
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PhotoUpdate(BaseModel):
    image_url_transform: str = Field(max_length=255)
    description: str = Field(max_length=500)
    tags: List[int] | None


# class PhotoBase(BaseModel):
#     description: Optional[str]

# class PhotoCreate(PhotoBase):
#     pass

# class PhotoOut(PhotoBase):
#     id: int
#     user_id: int
#     image_url: str

#     class Config:
#         from_attributes = True
