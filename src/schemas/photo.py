from datetime import datetime
from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional
import json


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


class CommentDisplay(BaseModel):
    user: str
    content: str
    created_at: datetime
    updated_at: datetime


class PhotoIn(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[str]] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        print(value)
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @validator("tags")
    def validate_tags(cls, tags):
        if tags is not None and len(tags) > 5:
            raise ValueError("Number of tags cannot exceed 5.")
        return tags


class PhotoCreate(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[int]] | None = None
    image_url: str = Field(max_length=255, default=None)


class PhotoOut(BaseModel):
    """
    Pydantic model representing output data for retrieving a photo.

    """

    id: int
    description: str = Field(max_length=500)
    tags: Optional[List[TagOut]] | None = None
    image_url: str = Field(max_length=255, default=None)
    image_url_transform: Optional[str] = Field(max_length=255)
    user_id: int
    created_at: datetime
    comments: Optional[List[CommentDisplay]]

    class Config:
        from_attributes = True


class PhotoUpdateIn(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[str]] | None = None
    image_url_transform: Optional[str] = Field(max_length=255, default=None)
    
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        print(value)
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @validator("tags")
    def validate_tags(cls, tags):
        if tags is not None and len(tags) > 5:
            raise ValueError("Number of tags cannot exceed 5.")
        return tags


class PhotoUpdateOut(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[int]] | None = None
    image_url_transform: Optional[str] = Field(max_length=255, default=None)


class TransformationInput(BaseModel):
    width: int
    height: int
    crop: str
    effect: str
    angle: int

    class Config:
        schema_extra = {
            "example": {
                "width": 100,
                "height": 150,
                "crop": "fill",
                "effect": "sepia",
                "angle": 45,
            }
        }
