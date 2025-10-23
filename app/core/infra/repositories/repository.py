from datetime import datetime
from typing import Any, List, Sequence, Tuple, Type
from venv import logger

from pydantic import BaseModel
from sqlalchemy import (
    CursorResult,
    Delete,
    Result,
    Select,
    Update,
    delete,
    desc,
    select,
    text,
    update,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.core.models.base import Base


class Repository[Model: Base, T: BaseModel](RepositoryInterface[T]):
    def __init__(self, db: AsyncSession, model: Type[Model], entity: Type[T]) -> None:
        self.model: type[Model] = model
        self.db: AsyncSession = db
        self.entity: type[T] = entity

    async def create(self, obj: BaseModel) -> T | None:
        model: Model = self.model(**obj.model_dump(exclude_unset=True))
        try:
            self.db.add(instance=model)
            await self.db.commit()
            await self.db.refresh(instance=model)

            return self.entity.model_validate(model)
        except IntegrityError as e:
            logger.error(e)
            return None

    async def find_one(self, obj: BaseModel) -> T | None:
        conditions: dict[str, Any] = obj.model_dump(exclude_unset=True)

        query: Select[Tuple[Model]] = select(self.model).where(
            self.model.deleted == False
        )

        for key, value in conditions.items():
            query = query.where(getattr(self.model, key) == value)

        result: Result[Tuple[Model]] = await self.db.execute(statement=query)
        data: Model | None = result.scalar()

        if data is None:
            return None

        return self.entity.model_validate(obj=data)

    async def find_many(
        self,
        limit: int,
        offset: int,
        sort_by: str,
        descending: bool,
        filter: BaseModel | None = None,
    ) -> list[T]:
        query: Select[Tuple[Model]] = select(self.model).where(
            self.model.deleted == False
        )

        if filter is not None:
            conditions: dict[str, Any] = filter.model_dump(exclude_unset=True)

            for key, value in conditions.items():
                query = query.where(getattr(self.model, key) == value)

        query = (
            query.limit(limit=limit)
            .offset(offset=offset)
            .order_by(
                desc(column=text(text=sort_by)) if descending else text(text=sort_by)
            )
        )

        result: Result[Tuple[Model]] = await self.db.execute(statement=query)
        data: Sequence[Model] = result.scalars().unique().all()

        return [self.entity.model_validate(obj=x) for x in data]

    async def update(self, conditions: BaseModel, obj: BaseModel) -> int:
        updates: dict[str, Any] = obj.model_dump(exclude_unset=True)
        conditions_attr: dict[str, Any] = conditions.model_dump(exclude_unset=True)

        query: Update = (
            update(table=self.model)
            .values(**updates)
            .where(self.model.deleted == False)
        )

        for key, value in conditions_attr.items():
            query = query.where(getattr(self.model, key) == value)

        result: CursorResult[Any] = await self.db.execute(statement=query)
        await self.db.commit()

        return result.rowcount

    async def delete(self, conditions: BaseModel) -> int:
        conditions_attr: dict[str, Any] = conditions.model_dump(exclude_unset=True)

        query: Update = (
            update(table=self.model)
            .values(deleted=True)
            .where(self.model.deleted == False)
        )

        for key, value in conditions_attr.items():
            query = query.where(getattr(self.model, key) == value)

        result: CursorResult[Any] = await self.db.execute(statement=query)
        await self.db.commit()

        return result.rowcount

    async def hard_delete(self, conditions: BaseModel) -> int:
        conditions_attr: dict[str, Any] = conditions.model_dump(exclude_unset=True)

        query: Delete = delete(table=self.model)

        for key, value in conditions_attr.items():
            query = query.where(getattr(self.model, key) == value)

        result: CursorResult[Any] = await self.db.execute(statement=query)
        await self.db.commit()

        return result.rowcount

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
    ) -> List[T]:
        if limit <= 0 or offset < 0:
            raise ValueError("Invalid limit or offset")

        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        if searchable_key and not searchable_value:
            raise ValueError("searchable_value required when searchable_key provided")

        query = select(self.model).where(self.model.deleted == False)

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
                getattr(self.model, searchable_key).ilike(f"%{searchable_value}%")
            )

        if not hasattr(self.model, sort_by):
            raise ValueError(f"Invalid sort_by column: {sort_by}")

        sort_column = getattr(self.model, sort_by)
        query = query.order_by(desc(sort_column) if descending else sort_column)

        query = query.limit(limit).offset(offset)
        # print(query)

        result = await self.db.execute(query)
        data = result.scalars().unique().all()
        return [self.entity.model_validate(obj=x) for x in data]

    async def insert_many(self, rows: List[T]) -> tuple[int, int]:
        inserted_count = 0
        skipped_count = 0

        for row in rows:
            model: Model = self.model(**row.model_dump(exclude_unset=True))
            self.db.add(model)
            try:
                await self.db.commit()
                inserted_count += 1
            except IntegrityError:
                await self.db.rollback()
                skipped_count += 1
                continue

        return inserted_count, skipped_count
