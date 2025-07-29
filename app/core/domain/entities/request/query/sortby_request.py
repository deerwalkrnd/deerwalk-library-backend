from pydantic import BaseModel


class SortByRequest(BaseModel):
    sort_by: str = "created_at"
    is_descending: bool = True
