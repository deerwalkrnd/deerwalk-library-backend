from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.domain.entities.user import User
from app.core.models.book_borrow import FineStatus


class BookBorrow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    user_id: Optional[str] = None
    book_copy_id: Optional[int] = None
    fine_accumulated: Optional[int] = None
    times_renewable: Optional[int] = None
    times_renewed: Optional[int] = None
    due_date: Optional[datetime] = None
    fine_status: Optional[FineStatus] = None
    returned: Optional[bool] = None
    returned_date: Optional[datetime] = None

    user: Optional[User] = None
