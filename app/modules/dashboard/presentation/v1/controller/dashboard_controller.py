from fastapi import Depends
from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.modules.book_borrows.infra.repositories.book_borrow_repository import (
    BookBorrowRepository,
)
from app.modules.bookmarks.infra.repositories.bookmark_repository import (
    BookmarkRepository,
)
from app.modules.dashboard.domain.entities.response.librarian_dashboard_response import (
    LibrarianDashboardResponse,
)
from app.modules.dashboard.domain.entities.response.student_dashboard_response import (
    StudentDashboardResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dashboard.domain.usecases.get_student_dashboard_info_use_case import (
    GetStudentDashboardInfoUseCase,
)


class DashboardController:
    def __init__(self) -> None:
        pass

    async def librarian_dashboard(
        self,
    ) -> LibrarianDashboardResponse:
        return LibrarianDashboardResponse()

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
