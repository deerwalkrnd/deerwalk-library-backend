from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import Base


class BookCopyModel(Base):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    unique_identifier: Mapped[Optional[str]] = mapped_column(index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    book = relationship("BookModel", back_populates="copies")
