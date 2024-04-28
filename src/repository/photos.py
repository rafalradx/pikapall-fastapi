from sqlalchemy.orm import Session
from src.database.models import Photo
from src.schemas.photo import PhotoIn, PhotoUpdate, PhotoOut
from typing import List


class PhotoRepository:
    def __init__(self, db: Session):
        """
        Initialize the PhotoRepository.

        :param db: The database session.
        """
        self.db = db

    async def create_photo(self, photo_data: PhotoIn, user_id: int) -> PhotoOut:
        """
        Create a new photo.

        :param photo_data: The data for the new photo.
        :param user_id: The ID of the user creating the photo.
        :return: The newly created Photo object.
        """
        new_photo = Photo(**photo_data.dict(), user_id=user_id)
        self.db.add(new_photo)
        await self.db.commit()
        return new_photo

    async def get_photo_by_id(self, photo_id: int) -> PhotoOut:
        """
        Retrieve a photo by its ID.

        :param photo_id: The ID of the photo to retrieve.
        :return: The Photo object if found, otherwise None.
        """
        return self.db.query(Photo).filter(Photo.id == photo_id).first()

    async def update_photo(
        self, photo_id: int, photo_data: PhotoUpdate, user_id: int
    ) -> PhotoOut:
        """
        Update a photo.

        :param photo_id: The ID of the photo to update.
        :param photo_data: The updated data for the photo.
        :param user_id: The ID of the user updating the photo.
        :return: The updated Photo object if found, otherwise None.
        """
        existing_photo = await self.get_photo_by_id(photo_id)
        if not existing_photo:
            return None
        for field, value in photo_data.dict(exclude_unset=True).items():
            setattr(existing_photo, field, value)
        await self.db.commit()
        return existing_photo

    async def delete_photo(self, photo_id: int, user_id: int) -> PhotoOut:
        """
        Delete a photo.

        :param photo_id: The ID of the photo to delete.
        :param user_id: The ID of the user deleting the photo.
        :return: The deleted Photo object if found, otherwise None.
        """
        existing_photo = await self.get_photo_by_id(photo_id)
        if not existing_photo:
            return None
        self.db.delete(existing_photo)
        await self.db.commit()
        return existing_photo

    async def get_all_photos(self) -> List[PhotoOut]:
        """
        Retrieve all photos.

        :return: A list of all Photo objects.
        """
        return self.db.query(Photo).all()

    async def search_photos_by_tag(self, tag: str) -> List[PhotoOut]:
        """
        Search photos by tag.

        :param tag: The tag to search for.
        :return: A list of Photo objects containing the specified tag.
        """
        return self.db.query(Photo).filter(Photo.tags.contains(tag)).all()

    async def filter_photos(
            self, tag: str = None, min_rating: int = None, start_date: str = None, end_date: str = None
    ) -> List[PhotoOut]:
        """
        Filter photos by various criteria.

        :param tag: The tag to filter by.
        :param min_rating: The minimum rating to filter by.
        :param start_date: The start date to filter by.
        :param end_date: The end date to filter by.
        :return: A list of Photo objects matching the filter criteria.
        """
        query = self.db.query(Photo)
        if tag:
            query = query.filter(Photo.tags.contains(tag))
        if start_date:
            query = query.filter(Photo.upload_date >= start_date)
        if end_date:
            query = query.filter(Photo.upload_date <= end_date)
        return query.all()
