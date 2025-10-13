from datetime import datetime

from pydantic import BaseModel


class BookReturnRequest(BaseModel):
    fine_paid: bool
    returned_date: datetime
