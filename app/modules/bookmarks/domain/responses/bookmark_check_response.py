from pydantic import BaseModel


class BookmarkCheckResponse(BaseModel):
    status: bool
