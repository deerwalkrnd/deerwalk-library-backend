from abc import ABC, abstractmethod
from typing import List

from app.modules.books.domain.requests.bulk_book_create_request import (
    BulkCreateBookRequest,
)
from app.modules.books.domain.responses.book_bulk_upload_skip_response import (
    BookBulkUploadSkipResponse,
)
from pydantic import BaseModel


class BookBulkUploadResult(BaseModel):
    books_created: int = 0
    books_updated: int = 0
    copies_added: int = 0
    duplicates_ignored: int = 0
    skipped: List[BookBulkUploadSkipResponse] = []


class BookBulkUploadServiceInterface(ABC):
    @abstractmethod
    async def bulk_upload(
        self, create_book_requests: List[BulkCreateBookRequest]
    ) -> BookBulkUploadResult:
        raise NotImplementedError
