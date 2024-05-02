import unittest
from unittest.mock import MagicMock
from src.database.models import Rating
from src.repository.ratings import RatingRepository
from datetime import datetime


class TestRatings(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.db_session = MagicMock()
        self.rating_repository = RatingRepository(db_session=self.db_session)

    async def test_create_rating(self):
        test_photo_id = 1
        test_user_id = 1
        test_rating = 4

        created_rating = await self.rating_repository.create_rating(
            photo_id=test_photo_id,
            user_id=test_user_id,
            rating=test_rating
        )
        self.assertEqual(created_rating.photo_id, test_photo_id)
        self.assertEqual(created_rating.user_id, test_user_id)
        self.assertEqual(created_rating.rating, test_rating)

    async def test_get_ratings(self):
        mock_rating_1 = Rating(id=1, photo_id=1, user_id=1, rating=4)
        mock_rating_2 = Rating(id=2, photo_id=2, user_id=2, rating=3)
        mock_ratings = [mock_rating_1, mock_rating_2]
        self.db_session.query.return_value.filter.return_value.all.return_value = mock_ratings
        result = await self.rating_repository.get_ratings()
        self.assertEqual(result, mock_ratings)

    async def test_get_rating_by_id(self):
        test_rating_id = 1
        mock_rating = Rating(
            id=test_rating_id, photo_id=1, user_id=1, rating=4)
        self.db_session.query.return_value.filter.return_value.first.return_value = mock_rating
        result = await self.rating_repository.get_rating_by_id(rating_id=test_rating_id)
        self.assertEqual(result, mock_rating)

    async def test_get_rating_by_id_not_found(self):
        test_rating_id = 999
        self.db_session.query.return_value.filter.return_value.first.return_value = None
        result = await self.rating_repository.get_rating_by_id(rating_id=test_rating_id)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
