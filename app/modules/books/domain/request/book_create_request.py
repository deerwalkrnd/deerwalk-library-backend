from typing import List, Optional
from pydantic import BaseModel


class CreateBookCopy(BaseModel):
    unique_identifer: str


class CreateBookRequest(BaseModel):
    title: str
    author: str
    publication: str
    isbn: str
    category: str
    genres: List[int]
    grade: str
    cover_image_url: str | None = None
    copies: Optional[List[CreateBookCopy]] = []
