from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GenreModel(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    title: Mapped[Optional[str]]
    image_url: Mapped[Optional[str]]
