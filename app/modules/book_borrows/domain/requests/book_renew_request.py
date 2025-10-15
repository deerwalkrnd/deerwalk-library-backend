from datetime import datetime

from pydantic import BaseModel


class BookRenewRequest(BaseModel):
    new_due_date: datetime
    fine_collected: int
