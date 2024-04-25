import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from src.database.models import Tag, User
from src.schemas.photo import TagIn, TagOut

from src.repository.tags import (
    get_tag,
    get_tags,
    create_or_get_tag,
    update_tag,
    delete_tag,
)


class TestTags(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        # self.user = User(id=1)

    async def test_get_tags(self):
        tags = [Tag(), Tag(), Tag()]
        self.session.query().filter().offset().limit().all.return_value = tags
        result = await get_tags(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, tags)

    async def test_get_tag_found(self):
        tag = Tag()
        self.session.query().filter().first.return_value = tag
        result = await get_tag(tag_id=1, user=self.user, db=self.session)
        self.assertEqual(result, tag)

    async def test_get_tag_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_tag(tag_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_tag(self):
        body = TagIn(name="Nature")
        result = await create_or_get_tag(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_tag(self):
        tag = Tag(id=1, name="Old Name")
        updated_body = TagIn(name="New Name")
        self.session.query().filter().first.return_value = tag
        result = await update_tag(tag_id=1, body=updated_body, user=self.user, db=self.session)

        self.assertEqual(result.id, tag.id)
        self.assertEqual(result.name, updated_body.name)

    async def test_remove_tag_found(self):
        tag = Tag()
        self.session.query().filter().first.return_value = tag
        result = await delete_tag(tag_id=1, user=self.user, db=self.session)
        self.assertEqual(result, tag)

    async def test_remove_tag_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await delete_tag(tag_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
