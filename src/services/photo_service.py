from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from src.database.models import Photo
from src.schemas.photo import PhotoCreate, PhotoUpdate
from src.services.auth_user import get_current_user
from src.services.cloudinary import upload_image_to_cloudinary


class PhotoService:
    def __init__(self, db: Session):
        self.db = db

    def get_photo_by_id(self, photo_id: int) -> Optional[Photo]:
        """
        Pobierz zdjęcie na podstawie jego identyfikatora.
        """
        return self.db.query(Photo).filter(Photo.id == photo_id).first()

    def create_photo(self, photo_data: PhotoCreate, current_user_id: int) -> Photo:
        """
        Dodaj nowe zdjęcie na podstawie danych przekazanych przez użytkownika.
        """
        new_photo = Photo(
            user_id=current_user_id,
            description=photo_data.description,
            created_at=datetime.now(),
        )
        self.db.add(new_photo)
        self.db.commit()
        self.db.refresh(new_photo)
        return new_photo

    def update_photo(self, photo: Photo, photo_data: PhotoUpdate) -> Photo:
        """
        Zaktualizuj istniejące zdjęcie na podstawie danych przekazanych przez użytkownika.
        """
        if photo_data.description:
            photo.description = photo_data.description
        self.db.commit()
        self.db.refresh(photo)
        return photo

    def delete_photo(self, photo: Photo) -> None:
        """
        Usuń istniejące zdjęcie.
        """
        self.db.delete(photo)
        self.db.commit()

    def upload_and_update_photo(self, photo: Photo, image_file) -> str:
        """
        Prześlij zdjęcie do usługi Cloudinary i zaktualizuj URL zdjęcia w bazie danych.
        """
        if image_file:
            try:
                cloudinary_url = upload_image_to_cloudinary(image_file)
                photo.image_url = cloudinary_url
                self.db.commit()
                return cloudinary_url
            except Exception as e:
                self.db.rollback()
                raise e
        else:
            raise ValueError("No image file provided")

    def get_all_photos(self, skip: int = 0, limit: int = 10) -> List[Photo]:
        """
        Pobierz listę wszystkich zdjęć z paginacją.
        """
        return self.db.query(Photo).offset(skip).limit(limit).all()
