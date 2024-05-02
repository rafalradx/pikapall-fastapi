from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.database.models import Photo, Tag
from src.schemas.photo import PhotoCreate, PhotoUpdateOut, PhotoOut
from typing import List, Optional
from src.repository.tags import TagRepository


class PhotoRepository:
    def __init__(self, db: Session):
        """
        Initialize the PhotoRepository.

        :param db: The database session.
        """
        self.db = db

    async def create_photo(self, photo_data: PhotoCreate, user_id: int) -> PhotoOut:
        """
        Create a new photo.

        :param photo_data: The data for the new photo.
        :param user_id: The ID of the user creating the photo.
        :return: The newly created Photo object.
        """
        tags = self.db.query(Tag).filter(Tag.id.in_(photo_data.tags)).all()
        new_photo = Photo(
            description=photo_data.description,
            tags=tags,
            image_url=photo_data.image_url,
            user_id=user_id,
        )
        self.db.add(new_photo)
        self.db.commit()
        self.db.refresh(new_photo)
        return new_photo

    async def get_photo_by_id(self, photo_id: int) -> PhotoOut:
        """
        Retrieve a photo by its ID.

        :param photo_id: The ID of the photo to retrieve.
        :return: The Photo object if found, otherwise None.
        """
        return self.db.query(Photo).filter(Photo.id == photo_id).first()

    async def update_photo(
        self, photo_id: int, photo_data: PhotoUpdateOut, user_id: int
    ) -> Optional[PhotoOut]:
        """
        Update a photo.

        :param photo_id: The ID of the photo to update.
        :param photo_data: The updated data for the photo.
        :param user_id: The ID of the user updating the photo.
        :return: The updated Photo object if found, otherwise None.
        """
        existing_photo = await self.get_photo_by_id(photo_id)
        if existing_photo:
            tags = self.db.query(Tag).filter(Tag.id.in_(photo_data.tags)).all()
            existing_photo.description = photo_data.description
            existing_photo.tags = tags
            existing_photo.image_url_transform = photo_data.image_url_transform
            self.db.commit()
            return existing_photo
        return None

    async def delete_photo(self, photo_id: int, user_id: int) -> Optional[PhotoOut]:
        """
        Delete a photo.

        :param photo_id: The ID of the photo to delete.
        :param user_id: The ID of the user deleting the photo.
        :return: The deleted Photo object if found, otherwise None.
        """
        existing_photo = await self.get_photo_by_id(photo_id)
        if existing_photo:
            if existing_photo.user_id == user_id:
                self.db.delete(existing_photo)
                try:
                    self.db.commit()
                    return existing_photo
                except Exception as e:
                    self.db.rollback()
                    raise HTTPException(
                        status_code=500, detail=f"Could not delete photo: {str(e)}"
                    )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="You don't have permission to delete this photo",
                )
        else:
            return None

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
        return self.db.query(Photo).filter(Photo.tags.any(Tag.name == tag)).all()

    async def filter_photos(
        self,
        tag: str = None,
        min_rating: int = None,
        start_date: str = None,
        end_date: str = None,
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
            query = query.filter(Photo.tags.any(Tag.name == tag))
        if start_date:
            query = query.filter(Photo.created_at >= start_date)
        if end_date:
            query = query.filter(Photo.created_at <= end_date)
        return query.all()
