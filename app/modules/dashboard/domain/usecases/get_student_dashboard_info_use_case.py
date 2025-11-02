from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)
from app.modules.bookmarks.domain.repositories.bookmark_repository_interface import (
    BookmarkRepositoryInterface,
)
from app.modules.dashboard.domain.entities.response.student_dashboard_response import (
    StudentDashboardResponse,
)


class GetStudentDashboardInfoUseCase:
    def __init__(
        self,
        book_borrow_repository: BookBorrowRepositoryInterface,
        bookmark_repository: BookmarkRepositoryInterface,
    ) -> None:
        self.book_borrow_repository = book_borrow_repository
        self.bookmark_repository = bookmark_repository

    async def execute(self, student_id: str) -> StudentDashboardResponse:
        dashoard_data = await self.book_borrow_repository.student_dashboard(
            student_id=student_id
        )
        borrowed_count = await self.bookmark_repository.get_bookmark_count(
            student_id=student_id
        )

        dashboard_response = StudentDashboardResponse.model_validate(dashoard_data)

        dashboard_response.saved_books = borrowed_count

        return dashboard_response
