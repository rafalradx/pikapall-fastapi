import pickle

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
import cloudinary
import cloudinary.uploader
from dependencies import get_users_repository, get_redis_client
from src.database.models import User
from src.services.auth import auth_service
from src.config import settings
from src.schemas.users import UserOut
from src.repository.abstract import AbstractUserRepository

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: OAuth2PasswordBearer = Depends(oauth2_scheme),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
    redis: Redis = Depends(get_redis_client),
) -> UserOut:
    """
    Get the current authenticated user.

    :param token: The OAuth2 token.
    :type token: str

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param redis: The Redis client.
    :type redis: Redis

    :param auth_service: The JWT handling service.
    :type auth_service: HandleJWT

    :return: The current authenticated user.
    :rtype: UserOut

    :raises HTTPException 401: If the credentials are invalid.
    """
    user_email = await auth_service.get_email_from_access_token(token=token)
    user = await redis.get(f"user:{user_email}")
    if user is not None:
        return pickle.loads(user)

    user = await users_repository.get_user_by_email(user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    await redis.set(f"user:{user_email}", pickle.dumps(user))
    await redis.expire(f"user:{user_email}", 900)
    return user


@router.get("/me", status_code=status.HTTP_200_OK)
async def read_users_me(
    current_user: User = Depends(get_current_user),
) -> UserOut:
    """
    Get the details of the current authenticated user.

    :param current_user: The current authenticated user.
    :type current_user: User

    :return: The details of the current authenticated user.
    :rtype: UserOut
    """
    return current_user


@router.patch("/avatar", response_model=UserOut)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(get_current_user),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
    redis: Redis = Depends(get_redis_client),
):
    """
    Update the avatar of the current authenticated user via cloudinary upload service

    :param file: The image file to upload as the new avatar.
    :type file: UploadFile

    :param current_user: The current authenticated user.
    :type current_user: User

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param redis: The Redis client.
    :type redis: Redis

    :return: The updated user with the new avatar.
    :rtype: UserOut
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    client = cloudinary.uploader.upload(
        file.file, public_id=f"NotesApp/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(f"NotesApp/{current_user.username}").build_url(
        width=250, height=250, crop="fill", version=client.get("version")
    )
    user = await users_repository.update_avatar(current_user.email, src_url)

    redis.set(f"user:{user.email}", pickle.dumps(user))
    return user
