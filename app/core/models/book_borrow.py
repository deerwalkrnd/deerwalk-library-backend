from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


class FineStatus(Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
    DISABLED = "DISABLED"


class BookBorrowModel(Base):
    __tablename__ = "book_borrows"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_copy_id: Mapped[int] = mapped_column(
        ForeignKey("book_copies.id"),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.uuid"),
        index=True,
    )
    fine_accumulated: Mapped[Optional[int]]
    fine_status: Mapped[FineStatus] = mapped_column(default=FineStatus.UNPAID)
    times_renewable: Mapped[Optional[int]]
    times_renewed: Mapped[Optional[int]]
    due_date: Mapped[Optional[datetime]]
    returned: Mapped[Optional[bool]] = mapped_column(default=False)
    returned_date: Mapped[Optional[datetime]]
    remark: Mapped[Optional[str]]

    book_copy: Mapped["BookCopyModel"] = relationship(  # type: ignore
        "BookCopyModel", back_populates="borrows", lazy="selectin"
    )

    user: Mapped["UserModel"] = relationship(  # type: ignore
        "UserModel", back_populates="borrows", lazy="selectin"
    )

    # __table_args__ = (
    #     # UniqueConstraint("book_copy_id", "user_id", name="uq_book_copy_user"),
    # )
