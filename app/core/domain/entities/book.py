from pydantic import BaseModel
from typing import Optional, List
    
from app.core.models.books import BookType
from app.core.domain.entities.genre import Genre

class Book(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    isbn: Optional[str] = None
    book_type: Optional[BookType] = None
    class_: Optional[str] = None
    genre: Optional[List[Genre]] = None