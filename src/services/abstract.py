from abc import ABC, abstractmethod
from src.schemas.users import UserIn, UserOut, UserChangeRole
from src.schemas.photo import TransformationInput


class AbstractImageProvider(ABC):
    """
    An abstract base class defining the interface for a image service.

    """

    @abstractmethod
    def upload(self, file, user: UserOut) -> str:
        """
        Retrieve a user from the repository based on the provided email.

        :param file: The email of the user to retrieve.
        :type email: str

        :return: ulr to uploade image
        :rtype: str
        """
        ...

    @abstractmethod
    def transform(self, url, transform: TransformationInput) -> str: ...
