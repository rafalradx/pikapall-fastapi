import pickle

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
import cloudinary
import cloudinary.uploader
from dependencies import get_users_repository, get_redis_client
from src.database.models import User
from src.services.auth import auth_service
from src.services.auth_user import get_current_user
from src.config import settings
from src.schemas.users import UserOut
from src.repository.abstract import AbstractUserRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def read_users_me(
    current_user: UserOut = Depends(get_current_user),
) -> UserOut:
    """
    Get the details of the current authenticated user.

    :param current_user: The current authenticated user.
    :type current_user: User

    :return: The details of the current authenticated user.
    :rtype: UserOut
    """
    return current_user
