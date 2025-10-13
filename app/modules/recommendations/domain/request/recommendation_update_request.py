from typing import Optional

from pydantic import BaseModel


class RecommendationUpdateRequest(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    note: Optional[str] = None
    book_title: Optional[str] = None
    cover_image_url: Optional[str] | None = None
