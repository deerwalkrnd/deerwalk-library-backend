from datetime import datetime
from typing import List

from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import \
    QuoteRepositoryInterface


class GetManyQuotesUseCase:
    def __init__(self, quote_repository: QuoteRepositoryInterface) -> None:
        self.quote_repository = quote_repository

    async def execute(
        self,
        page: int,
        limit: int,
        searchable_field: str | None,
        searchable_value: str | None,
        starts: datetime | None,
        ends: datetime | None,
    ) -> List[Quote]:
        offset = (page - 1) * limit
        quotes = await self.quote_repository.filter(
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
        return quotes
