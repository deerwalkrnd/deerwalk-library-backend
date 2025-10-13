from datetime import datetime
from typing import List
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.core.models.book_borrow import BookBorrowModel
from app.core.models.book_copy import BookCopyModel
from app.core.models.users import UserModel
from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrow.domain.repository.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)
from app.modules.book_borrow.domain.response.book_borrow_response_dto import (
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
