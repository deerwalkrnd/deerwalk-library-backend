from app.core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DssBookModel(Base):
    __tablename__ = "dss_books"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    book = relationship("BookModel", back_populates="dss_books")
