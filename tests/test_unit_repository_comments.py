import unittest
from fastapi import HTTPException, status
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import Comment
from src.schemas.users import UserIn
from src.repository.comments import CommentsRepository
from datetime import datetime, timedelta


class TestComments(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.comments_repository = CommentsRepository(db_session=self.session)
        # self.user = User(id=1)

    async def test_create_comment(self):
        test_photo_id = 1
        test_user_id = 1
        test_content = "My comment to first photo."
        test_created_at=datetime.now(),
        test_updated_at=datetime.now(),
        new_comment = Comment(
            photo_id=test_photo_id, 
            user_id=test_user_id, 
            content=test_content, 
            created_at=test_created_at, updated_at=test_updated_at
            )
        result = await self.comments_repository.create_comment(test_photo_id, test_user_id, test_content)
        self.assertEqual(result.photo_id, new_comment.photo_id)
        self.assertEqual(result.user_id, new_comment.user_id)
        self.assertEqual(result.content, new_comment.content)
        self.assertEqual(result.created_at, new_comment.created_at)
        self.assertEqual(result.updated_at, new_comment.updated_at)

    async def test_update_comment(self):
        test_photo_id = 1
        test_user_id = 1
        test_content = "My new comment to first photo."
        test_created_at=datetime.now()-timedelta(days=2),
        test_updated_at=datetime.now(),
        new_comment = Comment(
            photo_id=test_photo_id, 
            user_id=test_user_id, 
            content=test_content, 
            created_at=test_created_at, updated_at=test_updated_at
            )
        result = await self.comments_repository.update_comment(test_photo_id, test_user_id, test_content)
        self.assertEqual(result.photo_id, new_comment.photo_id)
        self.assertEqual(result.user_id, new_comment.user_id)
        self.assertEqual(result.content, new_comment.content)
        self.assertEqual(result.created_at, new_comment.created_at)
        self.assertEqual(result.updated_at, new_comment.updated_at)

    
if __name__ == "__main__":
    unittest.main()
