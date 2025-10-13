from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class BooksGenreModel(Base):
    __tablename__ = "books_genre"
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True, index=True
    )

    book: Mapped["BookModel"] = relationship("BookModel", back_populates="genres")  # type:ignore
    genre: Mapped["GenreModel"] = relationship("GenreModel", back_populates="books")  # type: ignore
