from typing import Optional
from pydantic import BaseModel


class BookCopy(BaseModel):
    id: Optional[int] = None
    book_id: Optional[int] = None
    unique_identifier: Optional[str] = None
