from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.domain.entities.user import User
from app.modules.books.domain.entities.book import Book


class BookReview(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: Optional[int] = None
    book_id: Optional[int] = None
    user_id: Optional[str] = None
    review_text: Optional[str] = None
    is_spam: Optional[bool] = None
    user: Optional[User] = None
    book: Optional[Book] = None
