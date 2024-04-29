import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from src.services.abstract import AbstractImageProvider
from src.schemas.users import UserOut


class CloudinaryImageProvider(AbstractImageProvider):
    def __init__(self, settings) -> None:
        self.config = cloudinary.config(
            cloud_name=settings["cloud_name"],
            api_key=settings["api_key"],
            api_secret=settings["api_secret"],
        )

    def upload(self, file: UploadFile, current_user: UserOut):
        client = cloudinary.uploader.upload(
            file.file, public_id=f"PikaPall/{current_user.username}", overwrite=True
        )
        src_url = cloudinary.CloudinaryImage(
            f"PikaPall/{current_user.username}"
        ).build_url(width=250, height=250, crop="fill", version=client.get("version"))
        return src_url

    def transform(self, url, transform):
        return "not working yet"

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
