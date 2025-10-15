from typing import List
from pydantic import BaseModel
from app.modules.books.domain.repository.response.book_bulk_upload_skip_response import (
    BookBulkUploadSkipResponse,
)


class BookBulkUploadResponse(BaseModel):
    inserted: int | None
    skipped: List[BookBulkUploadSkipResponse] | None
