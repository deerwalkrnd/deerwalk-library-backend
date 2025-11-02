from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import and_, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.core.models.book_borrow import BookBorrowModel, FineStatus
from app.core.models.book_copy import BookCopyModel
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)
from app.modules.book_borrows.domain.responses.book_borrow_response_dto import (
    BookBorrowResponseDTO,
)


class BookBorrowRepository(
    Repository[BookBorrowModel, BookBorrow], BookBorrowRepositoryInterface
):
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db, BookBorrowModel, BookBorrow)

    async def get_borrow_with_user_and_book(
        self,
        filter: BaseModel | None,
        limit: int,
        offset: int,
        sort_by: str,
        descending: bool,
        start_date: datetime | None,
        end_date: datetime | None,
        searchable_key: str | None,
        searchable_value: str | None,
    ) -> List[BookBorrowResponseDTO]:
        if limit <= 0 or offset < 0:
            raise ValueError("Invalid limit or offset")

        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        if searchable_key and not searchable_value:
            raise ValueError("searchable_value required when searchable_key provided")

        query = (
            select(BookBorrowModel)
            .options(
                selectinload(BookBorrowModel.user),
                selectinload(BookBorrowModel.book_copy).selectinload(
                    BookCopyModel.book
                ),
            )
            .where(BookBorrowModel.deleted == False)
        )

        if filter is not None:
            conditions = filter.model_dump(exclude_unset=True)
            for key, value in conditions.items():
                if not hasattr(self.model, key):
                    raise ValueError(f"Invalid filter key: {key}")
                query = query.where(getattr(self.model, key) == value)

        date_column = getattr(self.model, "created_at", None)
        if date_column is not None:
            if start_date:
                query = query.where(date_column >= start_date)
            if end_date:
                query = query.where(date_column <= end_date)

        if searchable_key and searchable_value:
            if not hasattr(self.model, searchable_key):
                raise ValueError(f"Invalid searchable_key: {searchable_key}")
            query = query.where(
                getattr(self.model, searchable_key).like(f"{searchable_value}%")
            )

        if not hasattr(self.model, sort_by):
            raise ValueError(f"Invalid sort_by column: {sort_by}")

        sort_column = getattr(self.model, sort_by)
        query = query.order_by(desc(sort_column) if descending else sort_column)

        query = query.limit(limit).offset(offset)

        print(query)

        result = await self.db.execute(query)
        data = result.scalars().unique().all()

        print(data)

        return [BookBorrowResponseDTO.model_validate(obj=x) for x in data]

    async def student_dashboard(self, student_id: str) -> dict[str, int | str]:
        data: dict[str, int | str] = {}
        
        # total borrowed count (all time)
        query = (
            select(func.count())
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False, 
                    self.model.user_id == student_id
                )
            )
        )
        result = await self.db.execute(query)
        data["borrowed_count"] = result.scalar() or 0
        
        # returned books count
        query = (
            select(func.count())
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.returned == True,
                    self.model.user_id == student_id,
                )
            )
        )
        result = await self.db.execute(query)
        data["returned_books_count"] = result.scalar() or 0
        
        # overdue books count 
        query = (
            select(func.count())
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.returned == False,
                    self.model.due_date < datetime.now(),
                    self.model.user_id == student_id,  
                )
            )
        )
        result = await self.db.execute(query)
        data["overdue_books_count"] = result.scalar() or 0
        
        # fine accumulated 
        query = (
            select(func.sum(self.model.fine_accumulated))
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.user_id == student_id,  
                )
            )
        )
        result = await self.db.execute(query)
        data["fine_levied"] = result.scalar() or 0
        
        # most borrowed category 
        query = (
            select(BookModel.category)
            .join(BookCopyModel, BookModel.id == BookCopyModel.book_id)
            .join(BookBorrowModel, BookBorrowModel.book_copy_id == BookCopyModel.id)
            .where(BookBorrowModel.user_id == student_id)
            .group_by(BookModel.category)
            .order_by(func.count(BookBorrowModel.id).desc())  
            .limit(1)
        )

        result = await self.db.execute(query)
        most_read_category = result.scalar()
        data["most_borrowed_category"] = most_read_category.value if most_read_category else "none"
        
        return data

    async def librarian_dashboard(self) -> dict[str, int]:
        data: dict[str, int] = {}
        # overdue books
        query = select(func.count(self.model.id)).where(
            and_(
                self.model.deleted == False,
                self.model.returned == False,
                self.model.due_date < datetime.now(),
            )
        )

        result = await self.db.execute(query)
        overdue_books_count = result.scalar() or 0

        data["overdue_books_count"] = overdue_books_count

        # total returned books
        query = select(func.count(self.model.id)).where(
            and_(self.model.deleted == False, self.model.returned == True)
        )

        result = await self.db.execute(query)
        returned_books_count = result.scalar() or 0

        data["returned_books_count"] = returned_books_count

        # currently issued books
        query = select(func.count(self.model.id)).where(
            and_(self.model.deleted == False, self.model.returned == False)
        )
        result = await self.db.execute(query)
        currently_issued_books_count = result.scalar() or 0

        data["currently_issued_books_count"] = currently_issued_books_count

        # total pending fines

        query = select(func.sum(self.model.fine_accumulated)).where(
            and_(
                self.model.deleted == False, self.model.fine_status == FineStatus.UNPAID
            )
        )

        result = await self.db.execute(query)
        total_pending_fines = result.scalar() or 0

        data["total_pending_fines"] = total_pending_fines

        return data
