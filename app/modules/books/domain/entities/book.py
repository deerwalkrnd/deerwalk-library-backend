from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.models.book import BookCategoryType


class Book(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    isbn: Optional[str] = None
    category: Optional[BookCategoryType] = None
    grade: Optional[str] = None
    cover_image_url: Optional[str] | None = None
