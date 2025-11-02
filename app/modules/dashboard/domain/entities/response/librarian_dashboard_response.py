from typing import Optional
from pydantic import BaseModel, ConfigDict


class LibrarianDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    overdue_books_count: Optional[int] = None
    currently_issued_books_count: Optional[int] = None
    returned_books_count: Optional[int] = None
    total_pending_fines: Optional[int] = None
    total_books: Optional[int] = None
    students_count: Optional[int] = None
