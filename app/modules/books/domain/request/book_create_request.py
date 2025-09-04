from pydantic import BaseModel


class CreateBookRequest(BaseModel):
    title: str
    author: str
    publication: str
    isbn: str
    category: str
    genre: str
    grade: str
    cover_image_url: str | None = None
