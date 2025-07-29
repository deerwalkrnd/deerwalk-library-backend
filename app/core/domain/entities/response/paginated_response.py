from typing import List

from pydantic import BaseModel


class PaginatedResponseMany[T](BaseModel):
    page: int
    total: int
    next: int
    items: List[T]
