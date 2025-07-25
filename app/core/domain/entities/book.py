from pydantic import BaseModel, ConfigDict
from typing import Optional, List
    
from app.core.models.books import BookType
from app.core.domain.entities.genre import Genre
from app.core.domain.entities.book_unit import BookUnit


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    isbn: Optional[str] = None
    book_type: Optional[BookType] = None
    class_: Optional[str] = None
    genre: Optional[List[Genre]] = None
    units: Optional[List[BookUnit]] = None
    book_code: Optional[str] = None