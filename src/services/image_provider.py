import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile
from src.schemas.users import UserOut
from src.schemas.photo import TransformationInput
from abc import ABC, abstractmethod


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


class CloudinaryImageProvider(AbstractImageProvider):
    def __init__(self, settings) -> None:
        self.config = cloudinary.config(
            cloud_name=settings["cloud_name"],
            api_key=settings["api_key"],
            api_secret=settings["api_secret"],
        )

    def transform(self, public_id: str, transform: TransformationInput) -> str:
        """
        Apply transformation to an image.

        :param url: URL of the image.
        :param transform: Transformation parameters.
        :return: Transformed image URL.
        """
        transformed_image_url = cloudinary.CloudinaryImage(public_id).build_url(
            **transform.model_dump()
        )
        return transformed_image_url

    def upload(self, file: UploadFile, current_user: UserOut) -> tuple[str, str]:
        """
        Uploads the file to Cloudinary and saves the transformed image URL.

        :param file: The file to upload.
        :param current_user: The current user.
        :return: Transformed image URL.
        """
        client = cloudinary.uploader.upload(
            file.file,
        )
        public_id = client.get("public_id")

        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            version=client.get("version")
        )

        return (src_url, public_id)

    def delete(self, public_id) -> None:
        """
        Deletes a transformed image from Cloudinary.

        :param public_id: Public ID of the image.
        """
        cloudinary.uploader.destroy(public_id, invalidate=True)
