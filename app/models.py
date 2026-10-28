# here we create database tables
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from datetime import datetime, timezone
from flask_login import UserMixin
from app.extensions import login_manager

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# association table / Link table
# It exists because posts and tags have a many-to-many relationship:
# A relational database can't store that in either table directly, so a third table holds the pairs:
post_tags = Table(
  "post_tags",
  db.metadata,
  Column('post_id', Integer, ForeignKey("posts.id"), primary_key=True),
  Column('tag_id', Integer, ForeignKey("tags.id"), primary_key=True)
  # Without it, the same post/tag pair can be inserted twice. Make the two columns a composite primary key:
)


class User(UserMixin, db.Model):
  __tablename__ = "users"
  ADMIN = "admin"
  AUTHOR = "author"
  READER = "reader"

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
  email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
  password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
  role: Mapped[str] = mapped_column(String(10), default=READER)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

  posts: Mapped[list['Post']] = relationship(back_populates="author", cascade="all, delete-orphan")
  comments: Mapped[list['Comment']] = relationship(back_populates="user", cascade="all, delete-orphan")

class Post(db.Model):
  __tablename__ = "posts"
  DRAFT = "draft"
  PUBLISHED = "published"

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  body: Mapped[str] = mapped_column(Text, nullable=False)
  status: Mapped[str] = mapped_column(String(20), default=DRAFT)
  author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
  )

  author: Mapped["User"] = relationship(back_populates="posts")
  comments: Mapped[list['Comment']] = relationship(back_populates="post", cascade="all, delete-orphan")
  tags: Mapped[list['Tag']] = relationship(secondary=post_tags, back_populates="posts")


class Comment(db.Model):
  __tablename__ = "comments"

  id: Mapped[int] = mapped_column(primary_key=True)
  body: Mapped[str] = mapped_column(Text, nullable=False)
  post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

  post: Mapped["Post"] = relationship(back_populates="comments")
  user: Mapped["User"] = relationship(back_populates="comments")


class Tag(db.Model):
  __tablename__ = "tags"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(50), unique=True)

  posts: Mapped[list["Post"]] = relationship(secondary=post_tags,  back_populates="tags")









