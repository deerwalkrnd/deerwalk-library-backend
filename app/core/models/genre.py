from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from enum import Enum
from .base import Base

class GenreEnum(Enum):
    ROMANCE: "ROMANCE"
    HORROR: "HORROR"
    FANTASY: "FANTASY"


class GenreModel(Base):

    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[GenreEnum] = mapped_column(Enum(GenreEnum))

    books: Mapped[List["BookModel"]] = relationship(
        "BookModel",
        secondary = "book_genres",
        back_populates="genres"
    )