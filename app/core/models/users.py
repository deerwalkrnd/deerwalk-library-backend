from enum import Enum
from typing import Optional
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4


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
    name: Mapped[Optional[str]]
    password: Mapped[Optional[str]]
    roll_number: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)
    graduating_year: Mapped[Optional[str]]
