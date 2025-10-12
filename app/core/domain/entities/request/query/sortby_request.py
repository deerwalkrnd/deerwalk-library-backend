from pydantic import BaseModel


# todo: rename this to `SortByParams` for ergonomics
class SortByRequest(BaseModel):
    sort_by: str = "created_at"
    is_descending: bool = True
