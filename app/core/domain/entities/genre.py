from pydantic import BaseModel,ConfigDict
from typing import Optional, List
from app.core.domain.entities.book import Book


class Genre(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None