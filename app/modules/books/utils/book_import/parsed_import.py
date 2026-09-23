from dataclasses import dataclass, field
from typing import List, Literal

from app.modules.books.domain.requests.bulk_book_create_request import (
    BulkCreateBookRequest,
)
from app.modules.books.domain.responses.book_bulk_upload_skip_response import (
    BookBulkUploadSkipResponse,
)


@dataclass
class ParsedBookImport:
    format: Literal["template", "register"]
    books: List[BulkCreateBookRequest] = field(default_factory=list)
    # Rows that could not become a book (missing title, bad category, ...).
    skipped: List[BookBulkUploadSkipResponse] = field(default_factory=list)
    # Rows repeated within the file itself.
    duplicates_ignored: int = 0
