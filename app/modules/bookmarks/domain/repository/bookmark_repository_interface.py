from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.bookmarks.domain.entities.bookmark import Bookmark


class BookmarkRepositoryInterface(RepositoryInterface[Bookmark]):
    async def filter_bookmark(
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
    ) -> List[Bookmark]:
        raise NotImplementedError
