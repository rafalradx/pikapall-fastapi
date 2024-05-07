from typing import AsyncGenerator
from src.repository.abstract import AbstractUserRepository
from src.services.image_provider import AbstractImageProvider, CloudinaryImageProvider
from src.services.pwd_handler import AbstractPasswordHashHandler, BcryptPasswordHandler
from src.database.db import get_db
from src.repository.users import UserRepository
from src.repository.photos import PhotoRepository
from src.repository.tags import TagRepository
from src.repository.comments import CommentsRepository
from src.repository.ratings import RatingRepository
from src.config import settings
from redis.asyncio import Redis
from contextlib import asynccontextmanager


def get_users_repository() -> AbstractUserRepository:
    return UserRepository(next(get_db()))


def get_photos_repository() -> PhotoRepository:
    return PhotoRepository(next(get_db()))


def get_tags_repository() -> TagRepository:
    return TagRepository(next(get_db()))


def get_rating_repository() -> RatingRepository:
    return RatingRepository(next(get_db()))


def get_comments_repository() -> CommentsRepository:
    return CommentsRepository(next(get_db()))


def get_image_provider() -> AbstractImageProvider:
    cloud_setting = {
        "cloud_name": settings.cloudinary_name,
        "api_key": settings.cloudinary_api_key,
        "api_secret": settings.cloudinary_api_secret,
    }
    return CloudinaryImageProvider(cloud_setting)


def get_password_handler() -> AbstractPasswordHashHandler:
    return BcryptPasswordHandler()


@asynccontextmanager
async def get_redis_client() -> AsyncGenerator[Redis, None]:
    """
    Context manager for getting a Redis client with the specified configuration.
    """
    redis_client = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=False,
    )
    try:
        yield redis_client
    finally:
        await redis_client.close()
