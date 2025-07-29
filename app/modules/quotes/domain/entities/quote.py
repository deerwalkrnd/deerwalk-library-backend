from typing import Optional

from pydantic import BaseModel, ConfigDict


class Quote(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: Optional[int] = None
    author: Optional[str] = None
    quote: Optional[str] = None
