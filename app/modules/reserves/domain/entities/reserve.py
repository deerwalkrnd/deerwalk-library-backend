from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.core.domain.entities.user import User
from app.core.models.book_reserve import BookReserveEnum
from app.modules.books.domain.entities.book_copy import BookCopy


class Reserve(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    book_copy_id: Optional[int] = None
    user_id: Optional[str] = None
    state: Optional[BookReserveEnum] = None
    due: Optional[datetime] = None
    remarks: Optional[str] = None

    book_copy: Optional[BookCopy] = None
    user: Optional[User] = None
