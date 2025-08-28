from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


from sqlalchemy.orm import Mapped, mapped_column


class PasswordResetTokenModel(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.uuid"))
    token: Mapped[Optional[str]] = mapped_column()
    expires_at: Mapped[Optional[datetime]] = mapped_column()

    user = relationship("UserModel", back_populates="password_reset_tokens")
