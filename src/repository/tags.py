from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import Tag


class TagRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    async def get_all_tags(self, skip: int, limit: int) -> list[Tag]:
        """
        Retrieve all tags.

        :param skip: The number of records to skip.
        :param limit: The maximum number of records to retrieve.
        :param db: The database session.
        :return: A list of Tag objects.
        """
        return self._db.query(Tag).offset(skip).limit(limit).all()

    async def get_tag_by_id(self, tag_id: int) -> Tag:
        """
        Retrieve a tag by its ID.

        :param tag_id: The ID of the tag to retrieve.
        :param db: The database session.
        :return: The Tag object with the specified ID.
        """
        return self._db.query(Tag).filter(Tag.id == tag_id).first()

    async def get_tag_by_name(self, tag_name: str) -> Tag:
        """
        Retrieve a tag by its name.

        :param tag_name: The name of the tag to retrieve.
        :param db: The database session.
        :return: The Tag object with the specified name.
        """
        return self._db.query(Tag).filter(Tag.name == tag_name).first()

    async def create_tag(self, tag_name: str) -> Tag:
        """
        Create a new tag.

        :param tag_name: The name of the tag.
        :param db: The database session.
        :return: The Tag object.
        """
        tag = self._db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            self._db.add(tag)
            self._db.commit()
            self._db.refresh(tag)
        return tag

    async def update_tag(self, tag_id: int, new_tag_name: str) -> Tag:
        """
        Update an existing tag.

        :param tag_id: The ID of the tag to update.
        :param new_tag_name: The new name of the tag.
        :param db: The database session.
        :return: The updated Tag object.
        """
        tag = self._db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            tag.name = new_tag_name
            self._db.commit()
        return tag

    async def delete_tag(self, tag_id: int) -> Optional[Tag]:
        """
        Delete a tag.

        :param tag_id: The ID of the tag to delete.
        :param db: The database session.
        :return: The deleted Tag object, or None if the tag was not found.
        """
        tag = self._db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            self._db.delete(tag)
            self._db.commit()
            return tag
        return None
