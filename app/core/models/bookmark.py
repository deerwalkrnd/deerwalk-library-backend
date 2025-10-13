from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

from .base import Base


class BookmarkModel(Base):
    __tablename__ = "bookmarks"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.uuid"))
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"))

    user = relationship("UserModel", back_populates="bookmarks", lazy="selectin")
    book = relationship("BookModel", back_populates="bookmarks", lazy="selectin")
