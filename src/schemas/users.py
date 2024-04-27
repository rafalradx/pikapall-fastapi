from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr


class RoleEnum(str, Enum):
    admin = "administrator"
    mod = "moderator"
    user = "standard"


class UserIn(BaseModel):
    """
    Pydantic model representing input data for creating a user.

    """

    username: str = Field(min_length=5, max_length=16, default="Jack Black")
    email: EmailStr = "user@user.com"
    password: str = Field(min_length=6, max_length=12, default="password")
    role: RoleEnum = RoleEnum.user


class UserOut(BaseModel):
    """
    Pydantic model representing output data for retrieving a user.

    """

    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    registration_date: datetime

    class Config:
        from_attributes = True


class UserChangeRole(BaseModel):
    role: RoleEnum


class Token(BaseModel):
    """
    Pydantic model representing authentication tokens.

    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
