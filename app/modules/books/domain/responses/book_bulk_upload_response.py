from typing import List, Literal

from pydantic import BaseModel

from app.modules.books.domain.responses.book_bulk_upload_skip_response import (
    BookBulkUploadSkipResponse,
)


class BookBulkUploadRespose(BaseModel):
    format: Literal["template", "register"]
    # New books created. Kept under its original name for existing clients.
    inserted: int
    # Books that already existed and received new copies from this file.
    books_updated: int = 0
    copies_added: int = 0
    # Rows repeated elsewhere in the file (e.g. the same copy listed on two
    # sheets) and copies already in the library; neither is an error.
    duplicates_ignored: int = 0
    skipped: List[BookBulkUploadSkipResponse] = []
