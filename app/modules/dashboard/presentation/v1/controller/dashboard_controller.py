from fastapi import Depends
from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.book_borrows.infra.repositories.book_borrow_repository import (
    BookBorrowRepository,
)
from app.modules.bookmarks.infra.repositories.bookmark_repository import (
    BookmarkRepository,
)
from app.modules.books.infra.repositories.book_repository import BookRepository
from app.modules.dashboard.domain.entities.response.librarian_dashboard_response import (
    LibrarianDashboardResponse,
)
from app.modules.dashboard.domain.entities.response.student_dashboard_response import (
    StudentDashboardResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dashboard.domain.usecases.get_librarian_dashboard_info_use_case import (
    GetLibrarianDashboardInfoUseCase,
)
from app.modules.dashboard.domain.usecases.get_student_dashboard_info_use_case import (
    GetStudentDashboardInfoUseCase,
)


class DashboardController:
    def __init__(self) -> None:
        pass

    async def librarian_dashboard(
        self, db: AsyncSession = Depends(get_db)
    ) -> LibrarianDashboardResponse:
        book_repository = BookRepository(db=db)
        book_borrow_repository = BookBorrowRepository(db=db)
        user_repository = UserRepository(db=db)

        get_librarian_dashboard_info_use_case = GetLibrarianDashboardInfoUseCase(
            book_repository=book_repository,
            book_borrow_repository=book_borrow_repository,
            user_repository=user_repository,
        )

        return await get_librarian_dashboard_info_use_case.execute()

    async def student_dashboard(
        self,
        db: AsyncSession = Depends(get_db),
        student_id: str = Depends(get_current_user),
    ) -> StudentDashboardResponse:
        book_borrow_repository = BookBorrowRepository(db=db)
        bookmark_repository = BookmarkRepository(db=db)

        get_student_dashboard_info_use_case = GetStudentDashboardInfoUseCase(
            bookmark_repository=bookmark_repository,
            book_borrow_repository=book_borrow_repository,
        )

        return await get_student_dashboard_info_use_case.execute(student_id=student_id)
