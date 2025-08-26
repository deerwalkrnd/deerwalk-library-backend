from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class TeacherRecommendationModel(Base):
    __tablename__ = "teacher_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    name:Mapped[str]
    designation:Mapped[str]
    note:Mapped[str]
    book_title:Mapped[str]
    cover_image_url:Mapped[Optional[str]]