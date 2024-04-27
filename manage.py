import argparse
import asyncio
from enum import Enum
from src.database.models import User
from src.schemas.users import UserIn
from src.repository.abstract import AbstractUserRepository
from src.services.pwd_handler import AbstractPasswordHashHandler
from dependencies import get_users_repository, get_password_handler
from sqlalchemy.orm import Session
from src.database.db import SessionLocal


class RoleEnum(str, Enum):
    admin = "administrator"
    mod = "moderator"
    user = "standard"


class AddUsersViaCLI:
    def __init__(
        self,
        db_session: Session,
        repository: AbstractUserRepository,
        password_handler: AbstractPasswordHashHandler,
    ) -> None:
        self.session = db_session
        self.users_repo = repository
        self.pass_handler = password_handler

    async def add_user(self, new_user: UserIn) -> UserIn:
        exist_user = await self.users_repo.get_user_by_email(new_user.email)
        if exist_user:
            raise ValueError("User with this email already exists")
        new_user.password = self.pass_handler.get_password_hash(new_user.password)
        new_user = User(**new_user.model_dump())
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user


# CLI function to parse command-line arguments and add user
async def add_admin_user_cli():
    parser = argparse.ArgumentParser(
        description="Add user with role 'admin' to the database"
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="Username of the user (minimum 5 characters)",
        required=True,
    )
    parser.add_argument("-e", "--email", type=str, help="Email address of the user")
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="Password of the user (minimum 6 characters)",
        required=True,
    )
    parser.add_argument(
        "-r", "--role", type=RoleEnum, choices=list(RoleEnum), help="Users role"
    )
    args = parser.parse_args()

    new_user = UserIn(
        username=args.username,
        email=args.email,
        password=args.password,
        role=args.role,
    )
    db_session = SessionLocal()
    user_db_adder = AddUsersViaCLI(
        db_session=db_session,
        repository=get_users_repository(),
        password_handler=get_password_handler(),
    )
    try:
        await user_db_adder.add_user(new_user)
        print("User added successfully.")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(add_admin_user_cli())
