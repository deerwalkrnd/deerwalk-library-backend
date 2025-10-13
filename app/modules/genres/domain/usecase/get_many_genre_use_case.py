from datetime import datetime
from typing import List

from app.modules.genres.domain.entity.genre import Genre
from app.modules.genres.domain.repository.genre_repository_interface import \
    GenreRepositoryInterface


class GetManyGenreUseCase:
    def __init__(self, genre_repository: GenreRepositoryInterface) -> None:
        self.genre_repository = genre_repository

    async def execute(
        self,
        page: int,
        limit: int,
        searchable_field: str | None,
        searchable_value: str | None,
        starts: datetime | None,
        ends: datetime | None,
    ) -> List[Genre]:
        offset = (page - 1) * limit
        genres = await self.genre_repository.filter(
            offset=offset,
            limit=limit,
            descending=True,
            sort_by="created_at",
            end_date=ends,
            start_date=starts,
            searchable_key=searchable_field,
            searchable_value=searchable_value,
            filter=None,
        )
        return genres
