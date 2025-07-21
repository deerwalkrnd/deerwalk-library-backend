from enum import Enum
from typing import Any, Dict, Optional

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from sqlalchemy.dialects.postgresql import JSONB

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

    email: Mapped[Optional[str]]
    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)
    graduating_year: Mapped[Optional[str]]
    image_url: Mapped[Optional[str]]
    user_metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB)
