from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class BookGenresModel(Base):
    __tablename__ = "book_genres"

    id: Mapped['int'] = mapped_column(primary_key=True, index=True)
    book_id: Mapped['int'] = mapped_column(ForeignKey("books.id"), primary_key=True, index=True)
    genre_id: Mapped['int'] = mapped_column(ForeignKey("genres.id"), primary_key=True, index=True)