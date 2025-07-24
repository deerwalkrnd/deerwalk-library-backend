from .base import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class BookUnitsModel(Base):
    __table_name__="book_units"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), index=True)

    book: Mapped["BookModel"] = relationship("BookModel", back_populates="units")