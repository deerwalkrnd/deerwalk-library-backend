from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookGenre(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id = Optional[int] = None
    genre_id = Optional[int] = None