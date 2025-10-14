from pydantic import BaseModel


class BookBulkUploadResponse(BaseModel):
    inserted: int | None
    skipped: int | None