from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.domain.entities.user import User
from app.modules.books.domain.entities.book import Book


class Bookmark(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: Optional[str] = None
    book_id: Optional[int] = None
    user: Optional[User] = None
    book: Optional[Book] = None
