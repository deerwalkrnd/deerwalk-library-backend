from enum import Enum
from typing import List, Optional
from app.core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BookCategoryType(Enum):
    ACADEMIC = "ACADEMIC"
    NON_ACADEMIC = "NON_ACADEMIC"
    REFERENCE = "REFERENCE"


class BookModel(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    title: Mapped[Optional[str]] = mapped_column(index=True)
    author: Mapped[Optional[str]] = mapped_column(index=True)
    publication: Mapped[Optional[str]] = mapped_column(index=True)
    isbn: Mapped[Optional[str]] = mapped_column(index=True)
    category: Mapped[BookCategoryType] = mapped_column(
        default=BookCategoryType.NON_ACADEMIC
    )
    genre: Mapped[Optional[str]] = mapped_column(index=True)
    grade: Mapped[Optional[str]] = mapped_column(index=True)
    cover_image_url: Mapped[Optional[str]] = mapped_column(index=True)

    copies : Mapped[List["BookCopyModel"]] = relationship(
        "BookCopyModel", back_populates="book", cascade="all, delete-orphan"
    )
