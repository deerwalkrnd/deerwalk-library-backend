from pydantic import BaseModel, ConfigDict


class StudentDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_books_borrowed: int | None = None
    total_returned_books: int | None = None
    overdue_books: int | None = None
    fine_levied: int | None = None
    saved_books: int | None = None
    most_borrowed_category: str | None = None
