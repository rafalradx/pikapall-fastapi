import unittest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.orm import Session
from src.repository.photos import PhotoRepository
from src.schemas.photo import PhotoCreate, PhotoUpdateOut
from src.database.models import Photo, Tag


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

    async def test_delete_photo(self):
        photo_id = 1
        existing_photo = Photo(id=photo_id)
        self.repository.get_photo_by_id = AsyncMock(return_value=existing_photo)

        result = await self.repository.delete_photo(photo_id, 1)

        self.assertEqual(result, existing_photo)

    async def test_get_all_photos(self):
        photos = [Photo(id=1), Photo(id=2)]
        self.db.query.return_value.all.return_value = photos

        result = await self.repository.get_all_photos()

        self.assertEqual(result, photos)

    async def test_search_photos_by_tag(self):
        tag = "test_tag"
        photos = [Photo(id=1), Photo(id=2)]
        self.db.query.return_value.filter.return_value.all.return_value = photos

        result = await self.repository.search_photos_by_tag(tag)

        self.assertEqual(result, photos)

    async def test_filter_photos(self):
        photos = [Photo(id=1), Photo(id=2)]
        self.db.query.return_value.all.return_value = photos

        result = await self.repository.filter_photos(
            tag="test_tag", start_date="2024-01-01", end_date="2024-05-01"
        )

        self.assertEqual(result, photos)


if __name__ == "__main__":
    unittest.main()
