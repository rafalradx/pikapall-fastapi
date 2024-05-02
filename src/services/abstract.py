from abc import ABC, abstractmethod
from src.schemas.users import UserOut
from src.schemas.photo import TransformationInput


class AbstractImageProvider(ABC):
    """
    An abstract base class defining the interface for a image service.

    """

    @abstractmethod
    def upload(self, file, user: UserOut) -> tuple[str, str]:
        """
        Retrieve a user from the repository based on the provided email.

        :param file: The email of the user to retrieve.
        :type email: str

        :return: tuple (url_to_image, cloudinary public_id)
        :rtype: (str,str)
        """
        ...

    @abstractmethod
    def transform(self, public_id: str, transform: TransformationInput) -> str:
        """
        Apply transformation to an image.

        :param public_id: identifier of an image.
        :param transform: Transformation parameters.
        :return: Transformed image URL.
        """
        ...

    @abstractmethod
    def delete(self, url: str) -> None:
        """
        Deletes an image from Cloudinary.

        :param public_id: Public ID (url) of the image.
        """
        ...
