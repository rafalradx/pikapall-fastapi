from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from src.database.models import Photo, Tag, Rating
from src.schemas.photo import PhotoCreate, PhotoUpdateOut, PhotoOut
from typing import List, Optional
from sqlalchemy import or_


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
            cloudinary_public_id=photo_data.cloudinary_public_id,
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
            self.db.commit()
            return existing_photo
        return None

    async def update_photo_trans_url(self, photo_id: int, url: str) -> PhotoOut:
        existing_photo = await self.get_photo_by_id(photo_id)
        if not existing_photo:
            return None
        existing_photo.image_url_transform = url
        self.db.commit()
        return existing_photo

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

    async def get_photos(
        self,
        keyword: str = None,
        created_after: str = None,
        created_before: str = None,
        avg_rating_above: str = None,
        avg_rating_below: str = None,
        user_id: int = None,
    ) -> List[PhotoOut]:
        """
        Filter photos by various criteria.

        :param tag: The tag to filter by.
        :param min_rating: The minimum rating to filter by.
        :param start_date: The start date to filter by.
        :param end_date: The end date to filter by.
        :return: A list of Photo objects matching the filter criteria.
        """
        word = f"%{keyword}%"

        query = self.db.query(Photo)
        if keyword:
            query = query.filter(
                or_(Photo.tags.any(Tag.name.ilike(word)), Photo.description.ilike(word))
            )
        if created_after:
            query = query.filter(Photo.created_at > created_after)
        if created_before:
            query = query.filter(Photo.created_at < created_before)
        if avg_rating_above:
            query = (
                query.outerjoin(Rating)
                .group_by(Photo.id)
                .having(func.avg(Rating.rating) > avg_rating_above)
            )
        if avg_rating_below:
            query = (
                query.outerjoin(Rating)
                .group_by(Photo.id)
                .having(func.avg(Rating.rating) < avg_rating_below)
            )
        if user_id:
            query = query.filter(Photo.user_id == user_id)
        return query.all()
