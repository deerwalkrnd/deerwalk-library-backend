from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    name: Mapped[Optional[str]]
    designation: Mapped[Optional[str]]
    note: Mapped[Optional[str]]
    book_title: Mapped[Optional[str]]
    cover_image_url: Mapped[Optional[str]]
