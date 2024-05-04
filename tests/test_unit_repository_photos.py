import unittest
from unittest.mock import AsyncMock, MagicMock, call
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.repository.photos import PhotoRepository
from src.schemas.photo import PhotoCreate, PhotoUpdateOut
from src.database.models import Photo, Tag, Rating
from datetime import datetime



class TestPhotoRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):

        self.db = MagicMock(spec=Session)
        self.repository = PhotoRepository(self.db)

    async def async_wrapper(self, func, *args, **kwargs):
        return await func(*args, **kwargs)

    async def test_create_photo(self):
        photo_data = PhotoCreate(
            description="Test Description", tags=[1, 2], image_url="test.jpg"
        )
        user_id = 1
        tags = [Tag(id=1), Tag(id=2)]
        self.db.query.return_value.filter.return_value.all.return_value = tags
        new_photo = Photo(
            description=photo_data.description,
            tags=tags,
            image_url=photo_data.image_url,
            user_id=user_id,
        )  # usuwamy ustawienie id
        self.db.add.return_value = new_photo

        result = await self.repository.create_photo(photo_data, user_id)

        self.assertIsNone(result.id)

    async def test_get_photo_by_id(self):
        photo_id = 1
        photo = Photo(id=photo_id)
        self.db.query.return_value.filter.return_value.first.return_value = photo

        result = await self.repository.get_photo_by_id(photo_id)

        self.assertEqual(result, photo)

    async def test_update_photo(self):
        photo_id = 1
        photo_data = PhotoUpdateOut(
            description="Updated Description",
            tags=[1, 2],
            image_url_transform="test_transform.jpg",
        )
        existing_photo = Photo(id=photo_id)
        self.repository.get_photo_by_id = AsyncMock(return_value=existing_photo)
        tags = [Tag(id=1), Tag(id=2)]
        self.db.query.return_value.filter.return_value.all.return_value = tags

        result = await self.repository.update_photo(photo_id, photo_data, 1)

        self.assertEqual(result, existing_photo)
        self.db.commit.assert_called_once()

    async def test_delete_photo_by_owner(self):
        photo_id = 1
        owner_id = 1
        existing_photo = Photo(id=photo_id, user_id=owner_id)
        self.repository.get_photo_by_id = AsyncMock(return_value=existing_photo)
        result = await self.repository.delete_photo(photo_id=photo_id, user_id=owner_id)
        self.assertEqual(result, existing_photo)

    async def test_delete_photo_not_owner(self):
        photo_id = 1
        owner_id = 5
        not_owner_id = 6
        existing_photo = Photo(id=photo_id, user_id=owner_id)
        self.repository.get_photo_by_id = AsyncMock(return_value=existing_photo)
        with self.assertRaises(HTTPException) as context:
            await self.repository.delete_photo(photo_id=photo_id, user_id=not_owner_id)
        self.assertTrue(
            "You don't have permission to delete this photo" in str(context.exception)
        )

    async def test_get_photos_no_filters(self):
        expected_result = []  
        self.db.query.return_value.filter.return_value.all.return_value = expected_result
        result = await self.repository.get_photos()
        self.db.query.assert_called_once_with(Photo)
        assert len(result) == len(expected_result)

    async def test_get_photos_with_avg_rating_above_filter(self):
        avg_rating_above = 4.5
        expected_query = (
            self.db.query.return_value.filter.return_value.all.return_value
        ) = []
        await self.repository.get_photos(avg_rating_above=avg_rating_above)
        self.db.query.assert_called_once_with(Photo)
        result = self.db.query.return_value.filter.return_value.all.return_value
        assert len(result) == len(expected_query)

    async def test_get_photos_with_avg_rating_below_filter(self):
        avg_rating_below = 3.5
        expected_query = (
            self.db.query.return_value.filter.return_value.all.return_value
        ) = []
        await self.repository.get_photos(avg_rating_below=avg_rating_below)
        self.db.query.assert_called_once_with(Photo)
        result = self.db.query.return_value.filter.return_value.all.return_value
        assert len(result) == len(expected_query)

    async def test_get_photos_with_created_after_filter(self):
        created_after = datetime(2024, 5, 1)
        expected_query = (
            self.db.query.return_value.filter.return_value.all.return_value
        ) = []
        await self.repository.get_photos(created_after=created_after)
        self.db.query.assert_called_once_with(Photo)
        result = self.db.query.return_value.filter.return_value.all.return_value
        assert len(result) == len(expected_query)

    async def test_get_photos_with_created_before_filter(self):
        created_before = datetime(2024, 5, 1)
        expected_query = (
            self.db.query.return_value.filter.return_value.all.return_value
        ) = []
        await self.repository.get_photos(created_before=created_before)
        self.db.query.assert_called_once_with(Photo)
        result = self.db.query.return_value.filter.return_value.all.return_value
        assert len(result) == len(expected_query)

    async def test_get_photos_with_keyword_filter(self):
        keyword = "landscape"
        expected_query = (
            self.db.query.return_value.filter.return_value.all.return_value
        ) = []
        await self.repository.get_photos(keyword=keyword)
        self.db.query.assert_called_once_with(Photo)
        result = self.db.query.return_value.filter.return_value.all.return_value
        assert len(result) == len(expected_query)

    async def test_get_photos_with_user_id_filter(self):
        user_id = 1
        expected_query = (
            self.db.query.return_value.filter.return_value.all.return_value
        ) = []
        await self.repository.get_photos(user_id=user_id)
        self.db.query.assert_called_once_with(Photo)
        result = self.db.query.return_value.filter.return_value.all.return_value
        assert len(result) == len(expected_query)

if __name__ == "__main__":
    unittest.main()
