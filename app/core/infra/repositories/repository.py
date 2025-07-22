from datetime import datetime
from typing import Any, List, Sequence, Tuple, Type
from venv import logger

from pydantic import BaseModel
from sqlalchemy import (CursorResult, Delete, Result, Select, Update, delete,
                        desc, select, text, update)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.repositories.repository_interface import \
    RepositoryInterface
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
        start_date: datetime,
        end_date: datetime,
    ) -> List[T]:
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
            .where(
                self.model.created_at >= start_date
                and self.model.created_at <= end_date
            )
        )

        result: Result[Tuple[Model]] = await self.db.execute(statement=query)
        data: Sequence[Model] = result.scalars().unique().all()

        return [self.entity.model_validate(obj=x) for x in data]
