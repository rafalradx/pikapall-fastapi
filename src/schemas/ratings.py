from pydantic import BaseModel
from datetime import datetime


class Rating(BaseModel):
    id: int
    photo_id: int
    user_id: int
    rating: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
