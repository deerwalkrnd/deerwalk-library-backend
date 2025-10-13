from datetime import datetime

from pydantic import BaseModel, Field


class BookBorrowRequest(BaseModel):
    times_renewable: int = Field(gt=1, lt=4, default=3)
    fine_enabled: bool
    due_date: datetime = Field(gt=datetime.now())
    user_uuid: str
