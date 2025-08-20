from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class EventModel(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    event_date: Mapped[datetime]
    image_url: Mapped[str]
