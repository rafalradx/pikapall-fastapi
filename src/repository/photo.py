from sqlalchemy.orm import Session
from src.database.models import Photo
from src.schemas.photo import PhotoCreate, PhotoUpdate, PhotoOut


class PhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_photo(self, photo_data: PhotoCreate, user_id: int) -> PhotoOut:
        new_photo = Photo(**photo_data.dict(), user_id=user_id)
        self.db.add(new_photo)
        await self.db.commit()
        return new_photo

    async def get_photo_by_id(self, photo_id: int) -> PhotoOut:
        return self.db.query(Photo).filter(Photo.id == photo_id).first()

    async def update_photo(
        self, photo_id: int, photo_data: PhotoUpdate, user_id: int
    ) -> PhotoOut:
        existing_photo = await self.get_photo_by_id(photo_id)
        if not existing_photo:
            return None
        for field, value in photo_data.dict(exclude_unset=True).items():
            setattr(existing_photo, field, value)
        await self.db.commit()
        return existing_photo

    async def delete_photo(self, photo_id: int, user_id: int) -> PhotoOut:
        existing_photo = await self.get_photo_by_id(photo_id)
        if not existing_photo:
            return None
        self.db.delete(existing_photo)
        await self.db.commit()
        return existing_photo

    async def get_all_photos(self) -> list[PhotoOut]:
        return self.db.query(Photo).all()


from sqlalchemy.orm import Session
from src.schemas.photo import PhotoCreate, PhotoUpdate, PhotoOut, PhotoIn
from src.database.models import User, Photo


class PhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_photo(self, photo_data: PhotoIn, user_id: int) -> PhotoOut:
        new_photo = Photo(**photo_data.dict(), user_id=user_id)
        self.db.add(new_photo)
        await self.db.commit()
        return new_photo

    async def get_photo_by_id(self, photo_id: int) -> PhotoOut:
        return self.db.query(Photo).filter(Photo.id == photo_id).first()

    async def update_photo(
        self, photo_id: int, photo_data: PhotoUpdate, user_id: int
    ) -> PhotoOut:
        existing_photo = await self.get_photo_by_id(photo_id)
        if not existing_photo:
            return None
        for field, value in photo_data.dict(exclude_unset=True).items():
            setattr(existing_photo, field, value)
        await self.db.commit()
        return existing_photo

    async def delete_photo(self, photo_id: int, user_id: int) -> PhotoOut:
        existing_photo = await self.get_photo_by_id(photo_id)
        if not existing_photo:
            return None
        self.db.delete(existing_photo)
        await self.db.commit()
        return existing_photo

    async def get_all_photos(self) -> list[PhotoOut]:
        return self.db.query(Photo).all()
