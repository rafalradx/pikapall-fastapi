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

def display_available_transformations():
    print("Dostępne transformacje:")
    print("1. Rozmiar (width, height)")
    print("2. Wycinanie (crop)")
    print("3. Efekt (effect)")
    print("4. Obrót (angle)")
    print("5. Rozmycie (blur)")




