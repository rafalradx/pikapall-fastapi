from src.repository.abstract import AbstractUserRepository
from src.services.pwd_handler import AbstractPasswordHashHandler, BcryptPasswordHandler
from src.database.db import SessionLocal
from src.repository.users import UserRepository
from src.repository.photos import PhotoRepository
from src.repository.tags import TagRepository
from src.repository.comments import CommentsRepository
from src.config import settings
from redis.asyncio import Redis


def get_users_repository() -> AbstractUserRepository:
    return UserRepository(SessionLocal())


def get_photos_repository() -> PhotoRepository:
    return PhotoRepository(SessionLocal())


def get_tags_repository() -> TagRepository:
    return TagRepository(SessionLocal())


def get_comments_repository() -> CommentsRepository:
    return CommentsRepository(SessionLocal())


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
