from datetime import datetime
from typing import List
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.core.models.book_copy import BookCopyModel
from app.core.models.reserve import BookReserveEnum, ReserveModel
from app.core.models.users import UserModel
from app.modules.reserves.domain.entities.reserve import Reserve
from app.modules.reserves.domain.repositories.reserves_repository_interface import (
    ReservesRepositoryInterface,
)


class ReservesRepository(
    Repository[ReserveModel, Reserve], ReservesRepositoryInterface
):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, ReserveModel, Reserve)

    async def get_reserves_by_book(self, user_id: str, book_id: int) -> Reserve | None:
        query = (
            select(ReserveModel)
            .join(BookCopyModel, ReserveModel.book_copy_id == BookCopyModel.id)
            .join(BookModel, BookCopyModel.book_id == BookModel.id)
            .where(ReserveModel.user_id == user_id)
            .where(ReserveModel.state == BookReserveEnum.RESERVED)
            .where(BookModel.id == book_id)
            .where(ReserveModel.deleted == False)
        )

        result = await self.db.execute(query)
        reserve = result.scalar()

        if not reserve:
            return None

        return Reserve.model_validate(reserve)

    async def filter(
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
    ) -> List[Reserve]:
        if limit <= 0 or offset < 0:
            raise ValueError("Invalid limit or offset")

        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        if searchable_key and not searchable_value:
            raise ValueError("searchable_value required when searchable_key provided")

        query = (
            select(self.model)
            .where(self.model.deleted == False)
            .join(BookCopyModel, self.model.book_copy_id == BookCopyModel.id)
            .join(UserModel, self.model.user_id == UserModel.uuid)
            .join(BookModel, BookCopyModel.book_id == BookModel.id)
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
            match searchable_key:
                case "student_name":
                    query = query.where(UserModel.name.ilike(f"%{searchable_value}%"))
                case "book_title":
                    query = query.where(BookModel.title.ilike(f"%{searchable_value}%"))
                case "book_copy_id":
                    try:
                        book_copy_id = int(searchable_value)
                    except ValueError as e:
                        raise e

                    query = query.where(BookCopyModel.id == book_copy_id)
                case "unique_identifier":
                    query = query.where(
                        BookCopyModel.unique_identifier.ilike(f"%{searchable_value}%")
                    )
                case _:
                    if not hasattr(self.model, searchable_key):
                        raise ValueError(f"Invalid searchable_key: {searchable_key}")
                    query = query.where(
                        getattr(self.model, searchable_key).ilike(
                            f"%{searchable_value}%"
                        )
                    )

        if not hasattr(self.model, sort_by):
            raise ValueError(f"Invalid sort_by column: {sort_by}")

        sort_column = getattr(self.model, sort_by)
        query = query.order_by(desc(sort_column) if descending else sort_column)

        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        data = result.scalars().unique().all()
        return [self.entity.model_validate(obj=x) for x in data]
