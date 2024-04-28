from sqlalchemy.orm import sessionmaker
from src.database.db import get_db
from src.database.models import Photo
import cloudinary.uploader
from src.config import settings


def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret
)


def apply_transformation(db_session, photo_id, transformation):
    photo = db_session.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        image_url = photo.image_url

        result = cloudinary.uploader.transformations(image_url, transformation)

        photo.image_url_transform = result["secure_url"]
        db_session.commit()

        return result["secure_url"]
    else:
        return None


def apply_transformation_endpoint(photo_id: int):
    transformation = {
        "width": 100,
        "height": 150,
        "crop": "fill",
        "effect": "sepia",
        "angle": 45
    }

    with get_db_session() as db_session:
        transformed_url = apply_transformation(db_session, photo_id, transformation)
        if transformed_url:
            return {"message": "Zdjęcie po zastosowaniu transformacji:", "transformed_url": transformed_url}
        else:
            return {"message": "Nie znaleziono zdjęcia o podanym ID."}
