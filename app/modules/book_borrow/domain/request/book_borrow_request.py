from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class BookBorrowRequest(BaseModel):
    book_copy_id: int
    times_renewable: Optional[int]
    fine_enabled: bool
    due_date: datetime
