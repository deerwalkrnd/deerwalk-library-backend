from typing import Optional

from pydantic import BaseModel


class BookBulkUploadSkipResponse(BaseModel):
    book_title: str
    reason: str
    sheet: Optional[str] = None
    row: Optional[int] = None
