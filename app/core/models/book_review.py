from typing import Optional

from sqlalchemy import ForeignKey, Index
from app.core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BookReviewModel(Base):
    __tablename__ = "book_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.uuid"), index=True)
    review_text: Mapped[Optional[str]] = mapped_column(index=True)
    is_spam: Mapped[bool] = mapped_column(default=False)

    book: Mapped["BookModel"] = relationship("BookModel", back_populates="reviews")  # type:ignore
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="reviews")  # type:ignore

    __table_args__ = (Index("idx_unique_book_user", "book_id", "user_id", unique=True),)
