from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.domain.entities.user import User


class BookBorrow(BaseModel):
    id: Optional[int]
    user_id: Optional[str]
    book_copy_id: Optional[int]
    file_accumulated: Optional[int]
    times_renewable: Optional[int]
    times_renewed: Optional[int]
    due_date: Optional[datetime]

    user: Optional[User]
