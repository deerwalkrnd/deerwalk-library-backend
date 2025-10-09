from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BookBorrowRequest(BaseModel):
    book_copy_id: int
    times_renewable: Optional[int] = Field(gt=1, lt=3)
    fine_enabled: bool
    due_date: datetime = Field(gt=datetime.now())
    user_uuid: str
