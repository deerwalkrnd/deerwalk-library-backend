from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.modules.books.domain.entities.book import Book


class BookCopy(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    book_id: Optional[int] = None
    unique_identifier: Optional[str] = None
    condition: Optional[str] = None
    is_available: Optional[bool] = None

    book: Optional[Book] = None
