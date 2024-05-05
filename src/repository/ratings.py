from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import Rating
from src.schemas.users import RoleEnum


class RatingRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

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
        )
        self._db.add(new_rating)
        self._db.commit()
        self._db.refresh(new_rating)
        return new_rating

    async def delete_rating(
        self, rating_id: int, user_role: RoleEnum, user_id: int
    ) -> bool:
        """
        Delete a rating.

        :param rating_id: The ID of the rating to delete.
        :param user_role: The role of the user attempting to delete the rating.
        :param user_id: The ID of the user attempting to delete the rating.
        :return: True if the rating was successfully deleted, False otherwise.
        """
        if user_role in [RoleEnum.admin, RoleEnum.mod]:
            rating = self._db.query(Rating).filter(Rating.id == rating_id).first()
            if rating:
                self._db.delete(rating)
                self._db.commit()
                return True
        else:
            rating = (
                self._db.query(Rating)
                .filter(Rating.id == rating_id, Rating.user_id == user_id)
                .first()
            )
            if rating:
                self._db.delete(rating)
                self._db.commit()
                return True
        return False

    async def get_ratings(self) -> Optional[list[Rating]]:
        """
        Retrieve all ratings.

        :return: The rating object if found, else None.
        """
        return self._db.query(Rating).filter().all()

    async def get_rating_by_id(self, rating_id: int) -> Optional[Rating]:
        """
        Retrieve a rating by its ID.

        :param rating_id: The ID of the rating to retrieve.
        :return: The rating object if found, else None.
        """
        return self._db.query(Rating).filter(Rating.id == rating_id).first()

    async def get_ratings_for_photo(self, photo_id: int) -> Optional[list[Rating]]:
        """
        Retrieve all ratings for a photo.

        :param photo_id: Photo ID.
        :return: List of ratings for a given photo.
        """
        return self._db.query(Rating).filter(Rating.photo_id == photo_id).all()

    async def get_user_ratings(self, user_id: int) -> Optional[list[Rating]]:
        """
        Retrieve the rating given by a user for a specific photo.

        :param photo_id: Photo ID.
        :param user_id: User ID.
        :return: The rating given by the user for the photo, if it exists.
        """
        return self._db.query(Rating).filter(Rating.user_id == user_id).all()

    async def get_user_rating_for_photo(
        self, photo_id: int, user_id: int
    ) -> Optional[Rating]:
        """
        Retrieve the rating given by a user for a specific photo.

        :param photo_id: Photo ID.
        :param user_id: User ID.
        :return: The rating given by the user for the photo, if it exists.
        """
        return (
            self._db.query(Rating)
            .filter(Rating.photo_id == photo_id, Rating.user_id == user_id)
            .first()
        )

    async def get_user_rating_by_id(
        self, rating_id: int, user_id: int
    ) -> Optional[Rating]:
        """
        Retrieve the rating given by a user for a specific photo.

        :param photo_id: Photo ID.
        :param user_id: User ID.
        :return: The rating given by the user for the photo, if it exists.
        """
        return (
            self._db.query(Rating)
            .filter(Rating.id == rating_id, Rating.user_id == user_id)
            .first()
        )
