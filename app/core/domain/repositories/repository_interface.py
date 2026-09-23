from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Sequence


class RepositoryInterface[T](ABC):
    @abstractmethod
    async def find_one(self, obj: T) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def find_many(
        self,
        limit: int,
        offset: int,
        sort_by: str,
        descending: bool,
        filter: T | None,
    ) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, obj: T) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, rows: Sequence[T]) -> List[int | None]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, conditions: T) -> int:
        raise NotImplementedError

    @abstractmethod
    async def hard_delete(self, conditions: T) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update(self, conditions: T, obj: T) -> int:
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        filter: T | None,
        limit: int,
        offset: int,
        sort_by: str,
        descending: bool,
        start_date: datetime | None,
        end_date: datetime | None,
        searchable_key: str | None,
        searchable_value: str | None,
    ) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def count(
        self,
        filter: T | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        searchable_key: str | None = None,
        searchable_value: str | None = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def insert_many(self, rows: List[T]) -> tuple[int, int]:
        raise NotImplementedError
