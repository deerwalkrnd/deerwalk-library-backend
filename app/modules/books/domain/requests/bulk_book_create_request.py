from typing import List, Optional

from pydantic import BaseModel

from app.core.models.book import BookCategoryType


class BulkCreateBookCopy(BaseModel):
    unique_identifier: str
    condition: Optional[str] = None


class BulkCreateBookRequest(BaseModel):
    """
    Request model for bulk book upload via CSV.
    Uses genre names (strings) instead of IDs for user-friendliness.
    """

    title: str
    author: str
    publication: str
    isbn: str
    category: BookCategoryType
    genres: List[str]  # Genre names instead of IDs
    grade: Optional[str]
    cover_image_url: str | None = None
    copies: List[BulkCreateBookCopy] = []
