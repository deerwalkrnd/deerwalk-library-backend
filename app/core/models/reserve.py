from typing import Optional
from app.core.models.book_copy import BookCopyModel
from app.core.models.users import UserModel
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from enum import Enum
from datetime import datetime, timedelta


class BookReserveEnum(Enum):
    RESERVED = "RESERVED"
    BORROWED = "BORROWED"
    BORROW_FAILED = "BORROW_FAILED"


def get_due_date() -> datetime:
    return datetime.now() + timedelta(days=3)


class ReserveModel(Base):
    __tablename__ = "book_reserves"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_copy_id: Mapped[int] = mapped_column(
        ForeignKey("book_copies.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    state: Mapped[Optional[BookReserveEnum]] = mapped_column(
        default=BookReserveEnum.RESERVED, nullable=True
    )
    due: Mapped[Optional[datetime]] = mapped_column(default=get_due_date, nullable=True)
    remarks: Mapped[Optional[str]]

    book_copy: Mapped[Optional[BookCopyModel]] = relationship(
        "BookCopyModel", back_populates="reserves", lazy="selectin"
    )
    user: Mapped[Optional[UserModel]] = relationship(
        "UserModel", back_populates="reserves", lazy="selectin"
    )
