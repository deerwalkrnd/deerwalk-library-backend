from typing import List
from pydantic import BaseModel

from app.modules.books.domain.responses.book_bulk_upload_skip_response import (
    BookBulkUploadSkipResponse,
)


class BookBulkUploadRespose(BaseModel):
    inserted: int | None
    skipped: List[BookBulkUploadSkipResponse]
