from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.modules.books.domain.entities.book_copy import BookCopy


class Book(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    genres: Optional[List[int]] = None
    grade: Optional[str] = None
    cover_image_url: Optional[str] | None = None
    copies: Optional[List[BookCopy]] = None
