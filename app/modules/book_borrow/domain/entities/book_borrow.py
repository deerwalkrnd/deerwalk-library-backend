from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.domain.entities.user import User


class BookBorrow(BaseModel):
    id: Optional[int] = None
    user_id: Optional[str] = None
    book_copy_id: Optional[int] = None
    fine_accumulated: Optional[int] = None
    times_renewable: Optional[int] = None
    times_renewed: Optional[int] = None
    due_date: Optional[datetime] = None

    user: Optional[User] = None
