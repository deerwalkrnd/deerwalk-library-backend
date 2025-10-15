from pydantic import BaseModel


class BookmarkCreateRequest(BaseModel):
    book_id: int
