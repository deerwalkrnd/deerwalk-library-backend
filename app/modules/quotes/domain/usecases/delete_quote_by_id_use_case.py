from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import (
    QuoteRepositoryInterface,
)


class DeleteQuoteByIdUseCase:
    def __init__(self, quote_repository: QuoteRepositoryInterface) -> None:
        self.quote_repository = quote_repository

    async def execute(self, id: int) -> None:
        await self.quote_repository.hard_delete(conditions=Quote(id=id))
