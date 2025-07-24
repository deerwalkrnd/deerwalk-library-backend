from pydantic import BaseModel,ConfigDict
from typing import Optional

class BookUnit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: Optional[int] = None