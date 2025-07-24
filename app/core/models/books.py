from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from enum import Enum

from .base import Base

class BookType(Enum):
    ACADEMIC="ACADEMIC"
    NONACADEMIC="NONACADEMIC"
    REFERENCE="REFERENCE"



class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key = True, index=True, unique=True)
    title: Mapped[Optional[str]] = mapped_column(index = True)
    author: Mapped[Optional[str]]
    isbn: Mapped[Optional[str]]
    book_type: Mapped[BookType] = mapped_column(Enum(BookType), default=BookType.ACADEMIC)
    class_: Mapped[Optional[int]] = mapped_column("class")


    genres: Mapped[List["GenreModel"]] = relationship("GenreModel", secondary="book_genres", back_populates="books")
    units: Mapped[List["BookUnitsModel"]] = relationship("BookUnitsModel", back_populates="book")




