from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.quote import QuoteModel
from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import (
    QuoteRepositoryInterface,
)


class QuoteRepository(Repository[QuoteModel, Quote], QuoteRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, QuoteModel, Quote)
