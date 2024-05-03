import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import Comment
from src.repository.comments import CommentsRepository
from src.schemas.comments import CommentIn, CommentOut, CommentUpdate
from src.schemas.users import RoleEnum
from datetime import datetime


class TestComments(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.comments_repository = CommentsRepository(db_session=self.session)
        self.comment_in = CommentIn(
            photo_id=1,
            content="My comment to first photo.",
            created_at=datetime.now(),
            updated_at=None,
        )
        self.comment_out = CommentOut(
            id=1,
            user_id=1,
            photo_id=1,
            content="My comment to first photo.",
            created_at=datetime.now(),
            updated_at=None,
        )

    async def test_create_comment(self):
        user_id = 1
        result = await self.comments_repository.create_comment(
            new_comment=self.comment_in, user_id=user_id
        )
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.content, self.comment_in.content)
        self.assertEqual(result.photo_id, self.comment_in.photo_id)

    async def test_update_comment(self):
        new_content = CommentUpdate(content="New comment content")
        self.session.query.return_value.filter.return_value.first.return_value = (
            self.comment_out
        )
        result = await self.comments_repository.update_comment(
            comment_id=1,
            new_content=new_content,
        )
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.updated_at)
        self.assertEqual(result.content, new_content.content)

    async def test_get_comment_by_id_found(self):
        comment = self.comment_out
        comment.id = 3
        self.session.query.return_value.filter.return_value.first.return_value = (
            self.comment_out
        )
        result = await self.comments_repository.get_comment_by_id(comment_id=3)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, comment.id)

    async def test_get_comment_by_id_not_found(self):
        self.session.query.return_value.filter.return_value.first.return_value = None
        result = await self.comments_repository.get_comment_by_id(comment_id=3)
        self.assertIsNone(result)

    async def test_get_comments_for_photo(self):
        comments = [Comment(), Comment(), Comment()]
        self.session.query.return_value.filter.return_value.all.return_value = comments
        result = await self.comments_repository.get_comments_for_photo(photo_id=2)
        self.assertEqual(result, comments)


if __name__ == "__main__":
    unittest.main()
