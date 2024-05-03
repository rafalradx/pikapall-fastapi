from src.repository.abstract import AbstractUserRepository
from src.services.image_provider import AbstractImageProvider, CloudinaryImageProvider
from src.services.pwd_handler import AbstractPasswordHashHandler, BcryptPasswordHandler
from src.database.db import SessionLocal
from src.repository.users import UserRepository
from src.repository.photos import PhotoRepository
from src.repository.tags import TagRepository
from src.repository.comments import CommentsRepository
from src.repository.ratings import RatingRepository
from src.config import settings
from redis.asyncio import Redis


def get_users_repository() -> AbstractUserRepository:
    return UserRepository(SessionLocal())


def get_photos_repository() -> PhotoRepository:
    return PhotoRepository(SessionLocal())


def get_tags_repository() -> TagRepository:
    return TagRepository(SessionLocal())


def get_rating_repository() -> RatingRepository:
    return RatingRepository(SessionLocal())


def get_comments_repository() -> CommentsRepository:
    return CommentsRepository(SessionLocal())


def get_image_provider() -> AbstractImageProvider:
    cloud_setting = {
        "cloud_name": settings.cloudinary_name,
        "api_key": settings.cloudinary_api_key,
        "api_secret": settings.cloudinary_api_secret,
    }
    return CloudinaryImageProvider(cloud_setting)


def get_password_handler() -> AbstractPasswordHashHandler:
    return BcryptPasswordHandler()


def get_redis_client() -> Redis:
    Redis()
    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=False,
    )
