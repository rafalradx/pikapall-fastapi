from sqlalchemy.orm import Session
from src.database.models import Comment
from datetime import datetime
from src.schemas.comments import CommentIn, CommentOut, CommentUpdate
from typing import Optional


class CommentsRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    async def create_comment(self, new_comment: CommentIn, user_id: int) -> CommentOut:
        """
        Function that creates a new comment for a photo.

        :param db: Database session.
        :param photo_id: Photo ID.
        :param user_id: The ID of the user who is adding the comment.
        :param content: Comment content.
        :return: A newly created comment object.
        """
        new_comment = Comment(
            photo_id=new_comment.photo_id,
            user_id=user_id,
            content=new_comment.content,
            created_at=datetime.now(),
            updated_at=None,
        )
        self._db.add(new_comment)
        self._db.commit()
        self._db.refresh(new_comment)
        return new_comment

    async def update_comment(
        self, comment_id: int, new_content: CommentUpdate
    ) -> CommentOut:
        """
        Function that updates the comment content.

        :param db: Database session.
        :param comment_id: The ID of the update comment.
        :param user_id: The ID of the user who is adding the comment.
        :param new_content: New comment content.
        :return: The updated comment object, or None if the user is not the author of the comment.
        """
        comment = self._db.query(Comment).filter(Comment.id == comment_id).first()
        comment.content = new_content.content
        comment.updated_at = datetime.now()
        self._db.commit()
        self._db.refresh(comment)
        return comment

    async def delete_comment(
        self,
        comment_id: int,
    ) -> CommentOut:
        """
        Function to remove a comment.

        :param db: Database session.
        :param comment_id: The ID of the comment to be deleted.
        :param user_id: The ID of the user deleting the comment.
        :param user_role: User role.
        :return: The deleted comment object if found, otherwise False.
        """
        comment = self._db.query(Comment).filter(Comment.id == comment_id).first()
        self._db.delete(comment)
        self._db.commit()
        return comment

    async def get_comments_for_photo(self, photo_id: int) -> Optional[list[CommentOut]]:
        """
        A function that returns all comments for a given photo.

        :param db: Database session.
        :param photo_id: Photo ID.
        :return: List of comments for a given photo.
        """
        if not photo_id:
            return self._db.query(Comment).all()

        return self._db.query(Comment).filter(Comment.photo_id == photo_id).all()

    async def get_comment_by_id(self, comment_id: int) -> Optional[CommentOut]:
        """
        A function that returns all comments for a given photo.

        :param db: Database session.
        :param photo_id: Photo ID.
        :return: List of comments for a given photo.
        """
        return self._db.query(Comment).filter(Comment.id == comment_id).first()
