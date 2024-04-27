from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database.models import Tag, User, Photo
from src.schemas.photo import TagIn


# tagi w aplikacji sa globalne, nie należa do usera
# według mnie nie potrzebujemy takich zapytan do bazy
# PhotoTag to jest ta pomocnicza tabela do relacji many-to-many,
# raczej nie powinnismy z niej korzystac bezposrednio

# tu bym po prostu zwracał wszystkie tagi

async def get_all_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    """
    Retrieve all tags.

    :param skip: The number of records to skip.
    :param limit: The maximum number of records to retrieve.
    :param db: The database session.
    :return: A list of Tag objects.
    """
    return db.query(Tag).offset(skip).limit(limit).all()


# tu bym zwracał wybrany tag za pomoca id
async def get_tag_by_id(tag_id: int, db: Session) -> Tag:
    """
    Retrieve a tag by its ID.

    :param tag_id: The ID of the tag to retrieve.
    :param db: The database session.
    :return: The Tag object with the specified ID.
    """
    return db.query(Tag).filter(Tag.id == tag_id).first()


# tylko create tag
async def create_tag(tag_name: str, db: Session) -> Tag:
    """
    Create a new tag.

    :param tag_name: The name of the tag.
    :param db: The database session.
    :return: The Tag object.
    """
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag

# update tag po id bez usera


async def update_tag(tag_id: int, new_tag_name: str, db: Session) -> Tag:
    """
    Update an existing tag.

    :param tag_id: The ID of the tag to update.
    :param new_tag_name: The new name of the tag.
    :param db: The database session.
    :return: The updated Tag object.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = new_tag_name
        db.commit()
    return tag


async def delete_tag(tag_id: int, db: Session) -> Optional[Tag]:
    """
    Delete a tag.

    :param tag_id: The ID of the tag to delete.
    :param db: The database session.
    :return: The deleted Tag object, or None if the tag was not found.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
        return tag
    return None
