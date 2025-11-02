from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import and_, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.core.models.book_borrow import BookBorrowModel
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

        query = (
            select(func.count())
            .select_from(self.model)
            .where(and_(self.model.deleted == False, self.model.user_id == student_id))
        )

        print(query)

        result = await self.db.execute(query)
        borrowed_count = result.scalar()

        if not borrowed_count:
            borrowed_count = 0

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
        returned_books_count = result.scalar()

        if not returned_books_count:
            returned_books_count = 0

        print(query)

        query = (
            select(func.count())
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.returned == False,
                    self.model.due_date < datetime.now(),
                )
            )
        )
        print(query)

        result = await self.db.execute(query)
        overdue_books_count = result.scalar()
        if not overdue_books_count:
            overdue_books_count = 0

        query = (
            select(func.sum(self.model.fine_accumulated))
            .select_from(self.model)
            .where(and_(self.model.deleted == False, self.model.returned == True))
        )
        print(query)

        result = await self.db.execute(query)
        fine_accumulated = result.scalar()
        if not fine_accumulated:
            fine_accumulated = 0

        query = (
            select(
                BookModel.category,
            )
            .join(BookCopyModel, BookModel.id == BookCopyModel.book_id)
            .join(BookBorrowModel, BookBorrowModel.book_copy_id == BookCopyModel.id)
            .where(BookBorrowModel.user_id == student_id)
            .group_by(BookModel.category)
            .order_by(func.coun(BookBorrowModel.id).desc())
            .limit(1)
        )
        print(query)

        result = await self.db.execute(query)
        most_read_category = result.scalar()

        if not most_read_category:
            most_read_category = "none"

        most_read_category = most_read_category

        data["most_borrowed_category"] = most_read_category.value  # type: ignore
        data["fine_levied"] = fine_accumulated
        data["overdue_books_count"] = overdue_books_count
        data["returned_books_count"] = returned_books_count
        data["borrowed_count"] = borrowed_count

        return data
