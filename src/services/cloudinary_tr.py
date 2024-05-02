import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile
from src.services.abstract import AbstractImageProvider
from src.schemas.users import UserOut
from src.schemas.photo import TransformationInput


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

        # transformation = {
        #     "width": transform.width,
        #     "height": transform.height,
        #     "crop": transform.crop,
        #     "effect": transform.effect,
        #     "angle": transform.angle,
        # }

        # transformed_image_url = cloudinary.CloudinaryImage(url).image(
        #     transformation=[{"effect": "sepia"}]
        # )
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
