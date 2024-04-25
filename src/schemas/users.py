from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from typing import Literal


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
