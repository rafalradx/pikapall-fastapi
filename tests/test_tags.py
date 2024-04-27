import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from src.database.models import Tag
from src.repository.tags import (
    get_all_tags,
    get_tag_by_id,
    create_tag,
    update_tag,
    delete_tag,
)


class TestTags(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_tags(self):
        tags = [Tag(), Tag(), Tag()]
        self.session.query().offset().limit().all.return_value = tags
        result = await get_all_tags(skip=0, limit=10, db=self.session)
        self.assertEqual(result, tags)

    async def test_get_tag_found(self):
        tag = Tag()
        self.session.query(Tag).filter(Tag.id == 1).first.return_value = tag
        result = await get_tag_by_id(tag_id=1, db=self.session)
        self.assertEqual(result, tag)

    async def test_get_tag_not_found(self):
        self.session.query(Tag).filter(Tag.id == 1).first.return_value = None
        result = await get_tag_by_id(tag_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_create_tag(self):
        tag_name = "Nature"
        new_tag = Tag(name=tag_name)
        self.session.query(Tag).filter(
            Tag.name == tag_name).first.return_value = None
        await create_tag(tag_name=tag_name, db=self.session)
        self.session.add.assert_called_once_with(unittest.mock.ANY)
        self.session.commit.assert_called_once()

    async def test_update_tag(self):
        tag = Tag(id=1, name="Old Name")
        updated_name = "New Name"
        self.session.query(Tag).filter(Tag.id == 1).first.return_value = tag
        await update_tag(tag_id=1, new_tag_name=updated_name, db=self.session)
        self.assertEqual(tag.name, updated_name)
        self.session.commit.assert_called_once()

    async def test_remove_tag_found(self):
        tag = Tag()
        self.session.query(Tag).filter(Tag.id == 1).first.return_value = tag
        result = await delete_tag(tag_id=1, db=self.session)
        self.assertEqual(result, tag)
        self.session.delete.assert_called_once_with(tag)
        self.session.commit.assert_called_once()

    async def test_remove_tag_not_found(self):
        self.session.query(Tag).filter(Tag.id == 1).first.return_value = None
        result = await delete_tag(tag_id=1, db=self.session)
        self.assertIsNone(result)
        self.session.commit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
