from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.quote import QuoteModel
from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import (
    QuoteRepositoryInterface,
)
from sqlalchemy import Result, select, func


class QuoteRepository(Repository[QuoteModel, Quote], QuoteRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        super().__init__(db, QuoteModel, Quote)

    async def get_random_quote(self) -> Quote | None:
        query = select(QuoteModel).order_by(func.random()).limit(1)

        result: Result[Tuple[QuoteModel]] = await self.db.execute(query)

        quote: QuoteModel | None = result.scalar()

        if quote is None:
            return None

        return Quote(id=quote.id, author=quote.author, quote=quote.quote)
