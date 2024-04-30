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
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", backref="photos")
    tags = relationship("Tag", secondary="photo_m2m_tags", backref="photos")
    comments = relationship("Comment", backref="photo")
    ratings = relationship("Rating", backref="photo")

    @hybrid_property
    def average_rating(self):
        total_ratings = sum(rating.rating for rating in self.ratings)
        num_ratings = len(self.ratings)
        if num_ratings > 0:
            return total_ratings / num_ratings
        else:
            return None


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(
        Enum("standard", "moderator", "administrator", name="role_types"),
        nullable=False,
    )
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    refresh_token = Column(String(255), nullable=True)
    comments = relationship("Comment", backref="user")
    ratings = relationship("Rating", backref="user")


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


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    photo_id = Column(
        Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    rating = Column(Integer, nullable=False, default=1)
    # created_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, onupdate=func.now())
