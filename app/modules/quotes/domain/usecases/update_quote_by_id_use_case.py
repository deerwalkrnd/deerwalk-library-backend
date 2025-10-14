from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import (
    QuoteRepositoryInterface,
)


class UpdateQuoteByIdUseCase:
    def __init__(self, quote_repostitory: QuoteRepositoryInterface) -> None:
        self.quote_repository = quote_repostitory

    async def execute(self, conditions: Quote, new: Quote) -> None:
        await self.quote_repository.update(conditions=conditions, obj=new)
