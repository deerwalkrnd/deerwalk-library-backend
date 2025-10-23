from typing import Optional
from pydantic import BaseModel


class BooleanResponse[T](BaseModel):
    value: bool
    data: Optional[T]
