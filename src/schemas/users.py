from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Literal


class UserIn(BaseModel):
    """
    Pydantic model representing input data for creating a user.

    """
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)

class UserOut(BaseModel):
    """
    Pydantic model representing output data for retrieving a user.

    """
    id: int
    username: str
    email: EmailStr
    role: Literal["standard", "moderator", "administrator"]
    created_at: datetime

class UserChangeRole(BaseModel):
    role: Literal["standard", "moderator", "administrator"]

class Token(BaseModel):
    """
    Pydantic model representing authentication tokens.

    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    """
    Pydantic model representing an email for confirm email request.

    """
    email: EmailStr
