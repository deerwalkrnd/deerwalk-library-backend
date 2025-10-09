from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


def generate_uuid() -> str:
    return str(uuid4())


class UserRole(Enum):
    STUDENT = "STUDENT"
    LIBRARIAN = "LIBRARIAN"


class UserModel(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(
        primary_key=True, index=True, unique=True, default=generate_uuid
    )

    name: Mapped[Optional[str]] = mapped_column(index=True)

    password: Mapped[Optional[str]]

    roll_number: Mapped[Optional[str]] = mapped_column(index=True)

    email: Mapped[Optional[str]] = mapped_column(unique=True, index=True)

    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)
    graduating_year: Mapped[Optional[str]]
    image_url: Mapped[Optional[str]]
    user_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)

    feedbacks = relationship("FeedbackModel", back_populates="user")
    password_reset_tokens = relationship(
        "PasswordResetTokenModel", back_populates="user"
    )

    bookmarks = relationship("BookmarkModel", back_populates="user")
    reviews = relationship(
        "BookReviewModel",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="noload",
    )
    borrows = relationship(
        "BookBorrowModel",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="noload",
    )
