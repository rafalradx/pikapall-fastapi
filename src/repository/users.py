from src.repository.abstract import AbstractUserRepository
from src.database.models import User
from src.schemas.users import UserIn, UserOut
from sqlalchemy.orm import Session
from src.schemas.users import RoleEnum


class UserRepository(AbstractUserRepository):
    def __init__(self, db_session: Session):
        """
        Initializes the UserRepository with the provided SQLAlchemy database session.

        :param db_session: The SQLAlchemy database session.
        :type db_session: Session
        """
        self._session = db_session

    async def get_first_user(self) -> UserOut:
        """
        Retrieve a first user from the database.

        :return: A UserOut object representing the first user.
        :rtype: UserOut
        """
        return self._session.query(User).first()

    async def get_user_by_email(self, email: str) -> UserOut:
        """
        Retrieve a user from the repository based on the provided email.

        :param email: The email of the user to retrieve.
        :type email: str

        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        return self._session.query(User).filter(User.email == email).first()

    async def get_user_by_id(self, user_id: int) -> UserOut:
        """
        Retrieve a user from the repository based on the provided id.

        :param user_id: The id of the user to retrieve.
        :type user_id: int

        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        return self._session.query(User).filter(User.id == user_id).first()

    async def create_user(self, new_user: UserIn) -> UserOut:
        """
        Create a new user in the repository with an avatar from Gravatar.

        :param new_user: The UserIn object representing the new user to be created.
        :type new_user: UserIn

        :return: A UserOut object representing the created user.
        :rtype: UserOut
        """
        user = await self.get_first_user()
        # if users table is empty create administrator
        if not user:
            user_role = RoleEnum.admin
        else:
            user_role = RoleEnum.user
        new_user = User(**new_user.model_dump())
        new_user.role = user_role
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)
        return new_user

    async def change_user_role(self, user_id: int, role: RoleEnum) -> UserOut | None:
        """
        Retrieve a first user from the database.
        :param email: The email of the user to retrieve.
        :type email: str
        :param body: The new role for the user.
        :type body: UserChangeRole
        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        user = await self.get_user_by_id(user_id)
        if role.value:
            user.role = role.value
        self._session.commit()
        self._session.refresh(user)
        return user

    async def update_token(self, user: User, token: str | None) -> None:
        """
        Update the refresh token for a user in the repository for authentication.

        :param user: The user object representing the user to update.
        :type user: User
        :param token: The new authentication token for the user.
                          None if the token should be removed.
        :type token: str

        :return: None
        """
        user.refresh_token = token
        self._session.commit()
