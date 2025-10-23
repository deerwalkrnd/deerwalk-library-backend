from pydantic import BaseModel


class ReserveBookRequest(BaseModel):
    book_copy_id: int
