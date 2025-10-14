from pydantic import BaseModel


class BookmarkCheckRequest(BaseModel):
    book_id: int
