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

    def transform(self, url, transform: TransformationInput):
        """
    Apply transformation to an image.

    This method takes the URL of an image and applies transformation parameters to it,
    generating a new URL for the transformed image.

    :param url: URL of the original image.
    :type url: str
    :param transform: Transformation parameters such as width, height, crop, effect, and angle
    :param width: The desired width of the transformed image in pixels. Defaults to None.
    :param height: The desired height of the transformed image in pixels. Defaults to None.
    :param crop: The type of cropping to apply to the image. Possible values are "fill", "fit", "scale", "thumb", "crop", "lfill", "limit", and "pad". Defaults to None.
    :param effect: The effect to apply to the image. Possible values are "sepia", "grayscale", "blur", "pixelate", "brightness", "contrast", "saturation", and "hue". Defaults to None.
    :param angle: The angle of rotation for the image in degrees. Defaults to None.
    :type transform: TransformationInput
    :return: URL of the transformed image.
    :rtype: str
        """

        transformation = {
            "width": transform.width,
            "height": transform.height,
            "crop": transform.crop,
            "effect": transform.effect,
            "angle": transform.angle
        }

        transformed_image = cloudinary.CloudinaryImage(url).build_url(**transformation)

        return transformed_image

    def upload(self, file: UploadFile, current_user: UserOut):
        """
        Uploads the file to Cloudinary and saves the transformed image URL.

        :param file: The file to upload.
        :param current_user: The current user.
        :return: Transformed image URL.
        """
        client = cloudinary.uploader.upload(
            file.file, public_id=f"PikaPall/{current_user.username}", overwrite=True
        )
        src_url = cloudinary.CloudinaryImage(
            f"PikaPall/{current_user.username}"
        ).build_url(width=250, height=250, crop="fill", version=client.get("version"))

        return src_url



    def delete_transformed_image(self, public_id):
        """
        Deletes a transformed image from Cloudinary.

        :param public_id: Public ID of the image.
        """
        # Usuwanie obrazu o podanym publicznym ID
        cloudinary.uploader.destroy(public_id, invalidate=True)


    # def apply_transformation(db_session, photo_id, transformation):
    #     photo = db_session.query(Photo).filter(Photo.id == photo_id).first()
    #     if photo:
    #         image_url = photo.image_url

    #         result = cloudinary.uploader.transformations(image_url, transformation)

    #         photo.image_url_transform = result["secure_url"]
    #         db_session.commit()

    #         return result["secure_url"]
    #     else:
    #         return None

    # def apply_transformation_endpoint(photo_id: int):
    #     transformation = {
    #         "width": 100,
    #         "height": 150,
    #         "crop": "fill",
    #         "effect": "sepia",
    #         "angle": 45,
    #     }
