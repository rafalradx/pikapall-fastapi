from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
import json
from src.schemas.comments import CommentOut
from src.schemas.tags import TagOut


class PhotoIn(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[str]] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @field_validator("tags")
    def validate_tags(cls, tags):
        if tags is not None and len(tags) > 5:
            raise ValueError("Number of tags cannot exceed 5.")
        return tags


class PhotoCreate(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[int]] | None = None
    image_url: str = Field(max_length=255, default=None)
    cloudinary_public_id: str = Field(max_length=255, default=None)


class PhotoOut(BaseModel):
    """
    Pydantic model representing output data for retrieving a photo.

    """

    id: int
    description: str = Field(max_length=500)
    tags: Optional[List[TagOut]] | None = None
    image_url: str = Field(max_length=255, default=None)
    cloudinary_public_id: str = Field(max_length=255, default=None)
    image_url_transform: Optional[str] = Field(max_length=255)
    user_id: int
    created_at: datetime
    average_rating: Optional[float]
    comments: Optional[List[CommentOut]] | None = None

    model_config = {"from_attributes": True}


class PhotoUpdateIn(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[str]] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @field_validator("tags")
    def validate_tags(cls, tags):
        if tags is not None and len(tags) > 5:
            raise ValueError("Number of tags cannot exceed 5.")
        return tags


class PhotoUpdateOut(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[int]] | None = None

    @field_validator("tags")
    def validate_tags(cls, tags):
        if tags is not None and len(tags) > 5:
            raise ValueError("Number of tags cannot exceed 5.")
        return tags


class TransformationInput(BaseModel):
    width: int | None = None
    height: int | None = None
    crop: str | None = None
    effect: str | None = None
    angle: int | None = None
    gravity: str | None = None
    radius: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "width": 250,
                "height": 250,
                "crop": "thumb",
                "effect": "sepia",
                "angle": 45,
                "gravity": "face",
                "radius": "max",
            }
        }
    }
