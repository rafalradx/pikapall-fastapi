from pydantic import BaseModel


class RatingIn(BaseModel):
    photo_id: int
    user_id: int
    rating: int


class RatingOut(RatingIn):
    id: int

    class Config:
        from_attributes = True
