from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import Rating
from datetime import datetime


class RatingRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    async def get_all_ratings(self, skip: int, limit: int) -> list[Rating]:
        """
        Retrieve all Ratings.

        :param skip: The number of records to skip.
        :param limit: The maximum number of records to retrieve.
        :return: A list of Ratings objects.
        """
        return self._db.query(Rating).offset(skip).limit(limit).all()

    async def get_rating_by_id(self, rating_id: int) -> Optional[Rating]:
        """
        Retrieve a rating by its ID.

        :param rating_id: The ID of the rating to retrieve.
        :return: The rating object if found, else None.
        """
        return self._db.query(Rating).filter(Rating.id == rating_id).first()

    async def create_rating(self, photo_id: int, user_id: int, rating: int):
        """
        Function that creates a new rating for a photo.

        :param photo_id: Photo ID.
        :param user_id: The ID of the user who is adding the rating.
        :param rating: The rating value (from 1 to 5 stars).
        :return: A newly created rating.
        """
        new_rating = Rating(
            photo_id=photo_id,
            user_id=user_id,
            rating=rating,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self._db.add(new_rating)
        self._db.commit()
        self._db.refresh(new_rating)
        return new_rating

    async def update_rating(self, rating_id: int, new_rating: int):
        """
        Update an existing rating.

        :param rating_id: The ID of the rating to update.
        :param new_rating: The new rating value.
        :return: The updated rating.
        """
        rating = self._db.query(Rating).filter(Rating.id == rating_id).first()
        if rating:
            rating.rating = new_rating
            rating.updated_at = datetime.now()
            self._db.commit()
        return rating

    async def delete_rating(self, rating_id: int) -> Optional[Rating]:
        """
        Delete a rating.

        :param rating_id: The ID of the rating to delete.
        :return: The deleted Rating object, or None if the rating was not found.
        """
        rating = self._db.query(Rating).filter(Rating.id == rating_id).first()
        if rating:
            self._db.delete(rating)
            self._db.commit()
            return rating
        return None

    async def get_ratings_for_photo(self, photo_id: int) -> Optional[list[Rating]]:
        """
        Retrieve all ratings for a photo.

        :param photo_id: Photo ID.
        :return: List of ratings for a given photo.
        """
        return self._db.query(Rating).filter(Rating.photo_id == photo_id).all()

    async def calculate_average_rating(self, photo_id: int) -> Optional[float]:
        """
        Calculate the average rating for a photo.

        :param photo_id: Photo ID.
        :return: The average rating, or None if there are no ratings for the photo.
        """
        ratings = await self.get_ratings_for_photo(photo_id)
        if not ratings:
            return None
        total_ratings = sum(rating.rating for rating in ratings)
        return total_ratings / len(ratings)
