from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FeedbackModel(Base):
    __tablename__ = "feedbacks"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.uuid"))
    subject: Mapped[Optional[str]] = mapped_column(index=True)
    feedback: Mapped[Optional[str]] = mapped_column(index=True)
    is_acknowledged: Mapped[Optional[bool]] = mapped_column(index=True, default=False)

    user = relationship("UserModel", back_populates="feedbacks", lazy="joined")
