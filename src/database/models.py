from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    Date,
    Boolean,
    Table,
    func,
    Enum,
    Text,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

photo_m2m_tag = Table(
    "photo_m2m_tags",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "photo_id", Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False
    ),
    UniqueConstraint("photo_id", "tag_id", name="unique_photo_tag"),
)


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(Text)
    image_url = Column(String(255), nullable=False)
    image_url_transform = Column(String(255), nullable=True)
    qr_code_url = Column(String(255))  # QRcode
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", backref="photos")
    tags = relationship("Tag", secondary="photo_m2m_tags", backref="photos")
    comments = relationship("Comment", backref="photo")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(
        Enum("standard", "moderator", "administrator", name="role_types"),
        nullable=False,
    )
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    refresh_token = Column(String(255), nullable=True)
    comments = relationship("Comment", backref="user")


# Model tagu
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    photo_id = Column(
        Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# # Tabela łącznikowa dla relacji Zdjęcie-Tagi
# class PhotoTag(Base):
#     __tablename__ = "photo_tags"

#     photo_id = Column(
#         Integer, ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True
#     )
#     tag_id = Column(
#         Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
#     )

#     UniqueConstraint("photo_id", "tag_id", name="unique_photo_tag")
# class Rating(Base):
#     __tablename__ = "ratings"
#
#     id = Column(Integer, primary_key=True)
#     photo_id = Column(
#         Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
#     )
#     user_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )
#     rating = Column(Integer, nullable=False)
#
#     UniqueConstraint("photo_id", "user_id", name="unique_photo_rating")

# class QRCode(Base):
#     __tablename__ = 'qr_codes'
#
#     id = Column(Integer, primary_key=True)
#     photo_id = Column(Integer, ForeignKey('photos.id', ondelete='CASCADE'), unique=True)
#     qr_code_url = Column(String(255), nullable=False)
#
#     photo = relationship("Photo", back_populates="qr_code")
