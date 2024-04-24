from pydantic import BaseModel
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
