from typing import List, Optional

from pydantic import BaseModel

from app.core.models.book import BookCategoryType


class BulkCreateBookCopy(BaseModel):
    unique_identifier: str
    condition: Optional[str] = None


class BulkCreateBookRequest(BaseModel):
    """
    One book parsed out of a bulk-import file (template CSV/XLSX or the
    library's accession register), together with the physical copies to add.

    Uses genre names (strings) instead of IDs for user-friendliness. Only the
    title is mandatory: the library's own register has plenty of books with no
    ISBN, author or publisher recorded, and the database allows that.
    """

    title: str
    author: Optional[str] = None
    publication: Optional[str] = None
    isbn: Optional[str] = None
    category: BookCategoryType = BookCategoryType.NON_ACADEMIC
    genres: List[str] = []  # Genre names instead of IDs
    grade: Optional[str] = None
    cover_image_url: Optional[str] = None
    copies: List[BulkCreateBookCopy] = []

    # Where the book came from, so a skipped book can be traced back.
    source_sheet: Optional[str] = None
    source_row: Optional[int] = None
