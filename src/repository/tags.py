from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database.models import Tag, User, Photo
from src.schemas.photo import TagIn


# tagi w aplikacji sa globalne, nie należa do usera
# według mnie nie potrzebujemy takich zapytan do bazy
# PhotoTag to jest ta pomocnicza tabela do relacji many-to-many,
# raczej nie powinnismy z niej korzystac bezposrednio

# tu bym po prostu zwracał wszystkie tagi
# async def get_tags(skip: int, limit: int, user: User, db: Session) -> List[Tag]:
#     """
#     Retrieve all tags that belong to a specific user.

#     :param skip: The number of records to skip.
#     :param limit: The maximum number of records to retrieve.
#     :param user: The user object that owns the tags.
#     :param db: The database session.
#     :return: A list of Tag objects.
#     """
#     return (
#         db.query(Tag)
#         .join(PhotoTag)
#         .join(Photo)
#         .filter(Photo.user_id == user.id)
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )

# tu bym zwracał wybrany tag za pomoca id
# async def get_tag(tag_id: int, user: User, db: Session) -> Tag:
#     """
#     Retrieve a specific tag that belongs to a user.

#     :param tag_id: The ID of the tag to retrieve.
#     :param user: The user object that owns the tag.
#     :param db: The database session.
#     :return: The Tag object with the specified ID.
#     """
#     return (
#         db.query(Tag)
#         .join(PhotoTag)
#         .join(Photo)
#         .filter(and_(Tag.id == tag_id, Photo.user_id == user.id))
#         .first()
#     )


# tylko create tag
async def create_or_get_tag(tag_name: str, user: User, db: Session) -> Tag:
    """
    Create a new tag or retrieve an existing one for a user.

    :param tag_name: The name of the tag.
    :param user: The user object that will own the tag.
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
# async def update_tag(tag_id: int, tag_name: str, user: User, db: Session) -> Tag:
#     """
#     Update an existing tag that belongs to a user.

#     :param tag_id: The ID of the tag to update.
#     :param tag_name: The new name of the tag.
#     :param user: The user object that owns the tag.
#     :param db: The database session.
#     :return: The updated Tag object.
#     """
#     tag = (
#         db.query(Tag)
#         .join(PhotoTag)
#         .join(Photo)
#         .filter(and_(Tag.id == tag_id, Photo.user_id == user.id))
#         .first()
#     )
#     if tag:
#         tag.name = tag_name
#         db.commit()
#     return tag

# delete tag bez usera
# async def delete_tag(tag_id: int, user: User, db: Session) -> None:
#     """
#     Delete a tag that belongs to a user.

#     :param tag_id: The ID of the tag to delete.
#     :param user: The user object that owns the tag.
#     :param db: The database session.
#     """
#     tag = (
#         db.query(Tag)
#         .join(PhotoTag)
#         .join(Photo)
#         .filter(and_(Tag.id == tag_id, Photo.user_id == user.id))
#         .first()
#     )
#     if tag:
#         db.delete(tag)
#         db.commit()
