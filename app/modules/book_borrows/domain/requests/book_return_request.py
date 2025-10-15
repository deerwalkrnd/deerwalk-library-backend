from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BookReturnRequest(BaseModel):
    fine_paid: bool
    returned_date: datetime
    remark: Optional[str]
