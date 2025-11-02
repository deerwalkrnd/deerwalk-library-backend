from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)
from app.modules.books.domain.repositories.book_repository_interface import (
    BookRepositoryInterface,
)
from app.modules.dashboard.domain.entities.response.librarian_dashboard_response import (
    LibrarianDashboardResponse,
)


class GetLibrarianDashboardInfoUseCase:
    def __init__(
        self,
        book_repository: BookRepositoryInterface,
        book_borrow_repository: BookBorrowRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> None:
        self.book_repository = book_repository
        self.book_borrow_repository = book_borrow_repository
        self.user_repository = user_repository

    async def execute(self) -> LibrarianDashboardResponse:
        data = await self.book_borrow_repository.librarian_dashboard()
        response = LibrarianDashboardResponse.model_validate(data)
        books_count = await self.book_repository.get_total_books_count()
        response.total_books = books_count
        response.students_count = await self.user_repository.get_students_count()
        return response
