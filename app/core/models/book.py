from enum import Enum
from typing import List, Optional

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


class BookCategoryType(Enum):
    ACADEMIC = "ACADEMIC"
    NON_ACADEMIC = "NON_ACADEMIC"
    REFERENCE = "REFERENCE"


class BookModel(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    title: Mapped[Optional[str]] = mapped_column(index=True)
    author: Mapped[Optional[str]] = mapped_column(index=True)
    publication: Mapped[Optional[str]] = mapped_column(index=True)
    isbn: Mapped[Optional[str]] = mapped_column(index=True, unique=True)
    category: Mapped[BookCategoryType] = mapped_column(
        default=BookCategoryType.NON_ACADEMIC
    )
    grade: Mapped[Optional[str]] = mapped_column(index=True)
    cover_image_url: Mapped[Optional[str]] = mapped_column(index=True)

    genres: Mapped[List["BooksGenreModel"]] = relationship(  # type: ignore
        "BooksGenreModel",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    copies: Mapped[List["BookCopyModel"]] = relationship(  # type: ignore
        "BookCopyModel",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    bookmarks = relationship("BookmarkModel", back_populates="book")
    reviews: Mapped[List["BookReviewModel"]] = relationship(  # type: ignore
        "BookReviewModel",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    __table_args__ = (
        Index("idx_book_title_author", "title", "author"),
        Index("idx_book_category_grade", "category", "grade"),
    )
