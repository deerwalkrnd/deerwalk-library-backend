from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QuoteModel(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author: Mapped[Optional[str]] = mapped_column(index=True)
    quote: Mapped[Optional[str]] = mapped_column(index=True)
