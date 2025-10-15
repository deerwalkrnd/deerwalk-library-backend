from typing import List, Optional

from pydantic import BaseModel

from app.core.models.book import BookCategoryType


class CreateBookCopy(BaseModel):
    unique_identifier: str
    condition: Optional[str] = None


class CreateBookRequest(BaseModel):
    title: str
    author: str
    publication: str
    isbn: str
    category: BookCategoryType
    genres: List[int]
    grade: Optional[str]
    cover_image_url: str | None = None
    copies: List[CreateBookCopy] = []
