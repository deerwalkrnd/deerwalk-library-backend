from datetime import datetime
from typing import List

from app.modules.bookmarks.domain.entities.bookmark import Bookmark
from app.modules.bookmarks.domain.repository.bookmark_repository_interface import \
    BookmarkRepositoryInterface


class GetBookmarkByUserIdUseCase:
    def __init__(self, bookmark_repository: BookmarkRepositoryInterface):
        self.bookmark_repository = bookmark_repository

    async def execute(
        self,
        page: int,
        limit: int,
        searchable_field: str | None,
        searchable_value: str | None,
        starts: datetime | None,
        ends: datetime | None,
        user_id: str | None,
    ) -> List[Bookmark]:
        offset = (page - 1) * limit
        bookmarks = await self.bookmark_repository.filter_bookmark(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            end_date=ends,
            start_date=starts,
            searchable_key=searchable_field,
            searchable_value=searchable_value,
            filter=Bookmark(user_id=user_id),
        )
        return bookmarks
