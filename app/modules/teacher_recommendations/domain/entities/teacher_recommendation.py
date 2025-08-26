from typing import Optional
from pydantic import BaseModel, ConfigDict


class TeacherRecommendation(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    name: str
    designation: str
    note: str
    book_title: str
    cover_image_url: Optional[str] | None = None
