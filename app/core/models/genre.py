from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class GenreModel(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    title: Mapped[Optional[str]]
    image_url: Mapped[Optional[str]]

    books: Mapped[List["BooksGenreModel"]] = relationship(  # type: ignore
        "BooksGenreModel", back_populates="genre"
    )
