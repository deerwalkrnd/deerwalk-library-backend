from typing import Optional
from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    genre: Optional[str] = None
    grade: Optional[str] = None
    cover_image_url: Optional[str] | None = None
