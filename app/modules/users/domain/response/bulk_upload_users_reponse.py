from pydantic import BaseModel


class BulkUploadUsersResponse(BaseModel):
    inserted: int | None
    skipped: int | None
