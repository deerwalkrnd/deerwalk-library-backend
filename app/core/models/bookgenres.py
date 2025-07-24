from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class BookGenres(Base):
    __tablename__ = "bookgenres"

    book_id: Mapped['str'] = mapped_column(ForeignKey("books.id"))
    genre_id: Mapped['str'] = mapped_column(ForeignKey("genre.id"))