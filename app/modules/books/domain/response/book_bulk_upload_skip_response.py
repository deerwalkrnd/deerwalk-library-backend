from pydantic import BaseModel


class BookBulkUploadSkipResponse(BaseModel):
    book_title: str
    reason: str