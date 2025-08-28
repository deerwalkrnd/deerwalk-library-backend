from pydantic import BaseModel


class CreateTeacherRecommendationRequest(BaseModel):
    name: str
    designation: str
    note: str
    book_title: str
    cover_image_url: str | None = None
