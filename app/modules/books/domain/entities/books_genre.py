from typing import Optional
from pydantic import BaseModel
from app.modules.books.domain.entities.book import Book
from app.modules.genres.domain.entity.genre import Genre


class BooksGenre(BaseModel):
    book_id: Optional[int] = None
    genre_id: Optional[int] = None

    book: Optional[Book] = None
    genre: Optional[Genre] = None
