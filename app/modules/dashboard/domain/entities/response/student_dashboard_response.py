from pydantic import BaseModel, ConfigDict


class StudentDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    most_borrowed_category: str | None = None
    fine_levied: int | None = None
    overdue_books_count: int | None = None
    returned_books_count: int | None = None
    borrowed_count: int | None = None
    saved_books: int | None = None
