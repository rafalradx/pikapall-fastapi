import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import Comment
from src.repository.comments import CommentsRepository
from src.schemas.users import RoleEnum

class TestComments(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.comments_repository = CommentsRepository(db_session=self.session)

    async def test_create_comment(self):
        test_photo_id = 1
        test_user_id = 1
        test_content = "My comment to first photo."
        await self.comments_repository.create_comment(test_photo_id, test_user_id, test_content)
        self.session.add.assert_called_once_with(unittest.mock.ANY)
        self.session.commit.assert_called_once()

    async def test_update_comment_by_yourself_found(self):
        test_comment_id = 1
        test_photo_id = 1
        test_user_id = 1
        test_content = "My comment to first photo."
        comment = Comment(
            id=test_comment_id, 
            photo_id=test_photo_id, 
            user_id=test_user_id, 
            content=test_content)
        test_new_content = "My new comment to first photo."
        self.session.query(Comment).filter(Comment.id == test_comment_id).first.return_value = comment
        await self.comments_repository.update_comment(
            comment_id=test_comment_id, 
            user_id=test_user_id, 
            new_content=test_new_content)
        self.assertEqual(comment.content, test_new_content)
        self.session.commit.assert_called_once()

    async def test_update_comment_by_yourself_not_found(self):
        test_comment_id = 1
        test_user_id = 1
        test_new_content = "My new comment to first photo."
        self.session.query(Comment).filter(
            Comment.id == test_comment_id).first.return_value = None
        result = await self.comments_repository.update_comment(comment_id=test_comment_id, 
            user_id=test_user_id, 
            new_content=test_new_content)
        self.assertIsNone(result)
    
    async def test_delete_comment_by_Admin(self):
        test_comment_id = 1
        test_user_role = RoleEnum.admin
        comment = Comment(id=test_comment_id)
        self.session.query(Comment).filter(Comment.id == test_comment_id).first.return_value = comment
        result = await self.comments_repository.delete_comment(comment_id=test_comment_id, user_role=test_user_role)
        self.assertEqual(result, comment)
        self.session.delete.assert_called_once_with(comment)
        self.session.commit.assert_called_once()

    async def test_delete_comment_by_Moderator(self):
        test_comment_id = 1
        test_user_role = RoleEnum.mod
        comment = Comment(id=test_comment_id)
        self.session.query(Comment).filter(Comment.id == test_comment_id).first.return_value = comment
        result = await self.comments_repository.delete_comment(comment_id=test_comment_id, user_role=test_user_role)
        self.assertEqual(result, comment)
        self.session.delete.assert_called_once_with(comment)
        self.session.commit.assert_called_once()

    async def test_delete_comment_by_yourself(self):
        test_comment_id = 1
        test_user_role = RoleEnum.user
        result = await self.comments_repository.delete_comment(comment_id=test_comment_id, user_role=test_user_role)
        self.assertEqual(result, False)

    async def test_delete_comment_not_found(self):
        test_comment_id = 1
        test_user_role = RoleEnum.mod
        self.session.query(Comment).filter(Comment.id == test_comment_id).first.return_value = None
        result = await self.comments_repository.delete_comment(comment_id=test_comment_id, user_role=test_user_role)
        self.assertEqual(result, False)

    async def test_get_comments_for_photo(self):
        test_photo_id = 1
        comments = [Comment, Comment, Comment]
        self.session.query(Comment).filter(Comment.photo_id == test_photo_id).all.return_value = comments
        result = await self.comments_repository.get_comments_for_photo(photo_id=test_photo_id)
        self.assertEqual(result, comments)

if __name__ == "__main__":
    unittest.main()
