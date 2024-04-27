from abc import ABC, abstractmethod
from src.schemas.users import UserIn, UserOut, UserChangeRole


class AbstractUserRepository(ABC):
    """
    An abstract base class defining the interface for a user repository.

    Concrete implementations of this class must provide implementations for
    the abstract methods defined here.

    """

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserOut:
        """
        Retrieve a user from the repository based on the provided email.

        :param email: The email of the user to retrieve.
        :type email: str

        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        ...

    @abstractmethod
    def change_user_role(self, email: str, role: UserChangeRole) -> UserOut:
        """
        Change role of a user identified by email

        :param email: The email of the user subjected to role change.
        :type email: str

        :param role: Model describing new role
        :type role: UserChangedRole

        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        ...

    @abstractmethod
    def get_user_by_id(self, id: int) -> UserOut:
        """
        Retrieve a user from the repository based on the provided id.

        :param id: The id of the user to retrieve.
        :type id: int

        :return: A UserOut object representing the retrieved user.
        :rtype: UserOut
        """
        ...

    @abstractmethod
    def create_user(self, new_user: UserIn) -> UserOut:
        """
        Create a new user in the repository.

        :param new_user: The UserIn object representing the new user to be created.
        :type new_user: UserIn

        :return: A UserOut object representing the created user.
        :rtype: UserOut
        """
        ...

    @abstractmethod
    def update_token(self, user: UserOut, token: str | None) -> None:
        """
        Update the authentication token for a user in the repository.

        :param user: The user object representing the user to update.
        :type user: UserOut
        :param token: The new authentication token for the user.
                          None if the token should be removed.
        :param toke: str

        :return: None
        """
        ...
