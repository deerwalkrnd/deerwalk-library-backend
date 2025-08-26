from typing import Optional
from pydantic import BaseModel


class TeacherRecommendationUpdateRequest(BaseModel):
    name: str
    designation: str
    note: str
    book_title: str
    cover_image_url: Optional[str] | None = None