from datetime import datetime
from pydantic import BaseModel, Field

from typing import List

class TagIn(BaseModel):
    name: str = Field(max_length=25)

class TagOut(TagIn):
    id: int

    class Config:
        orm_mode = True

class CommentIn(BaseModel):
    content: str = Field(max_length=255)
    photo_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class CommentOut(CommentIn):
    id: int

    class Config:
        orm_mode = True

class PhotoIn(BaseModel):
    """
    Pydantic model representing input data for creating a photo.

    """
    image_url: str = Field(max_length=255)
    description: str = Field(max_length=500)
    tags: List[int] | None

class PhotoOut(PhotoIn):
    """
    Pydantic model representing output data for retrieving a photo.

    """
    id: int
    image_url_transform: str = Field(max_length=255)
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = Truefrom pydantic import BaseModel
from typing import List, Optional

class PhotoBase(BaseModel):
    description: Optional[str]

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(PhotoBase):
    pass

class PhotoOut(PhotoBase):
    id: int
    user_id: int
    image_url: str

    class Config:
        orm_mode = True
