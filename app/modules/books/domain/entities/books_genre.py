from typing import Optional
from pydantic import BaseModel, ConfigDict


class BooksGenre(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: Optional[int] = None
    genre_id: Optional[int] = None

    # book: Optional[Book] = None
    # genre: Optional[Genre] = None
