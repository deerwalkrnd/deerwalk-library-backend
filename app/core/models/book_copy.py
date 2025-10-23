from typing import Optional

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


class BookCopyModel(Base):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    unique_identifier: Mapped[Optional[str]] = mapped_column(index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    is_available: Mapped[Optional[bool]] = mapped_column(default=True)
    condition: Mapped[Optional[str]]

    book: Mapped["BookModel"] = relationship(  # type: ignore
        "BookModel", back_populates="copies", lazy="selectin"
    )  # type: ignore

    borrows: Mapped[list["BookBorrowModel"]] = relationship(  # type: ignore
        "BookBorrowModel", back_populates="book_copy"
    )  # type: ignore

    reserves: Mapped[list["ReserveModel"]] = relationship(  # type: ignore
        "ReserveModel", back_populates="book_copy"
    )

    __table_args__ = (Index("idx_book_copy_availability", "book_id", "is_available"),)
