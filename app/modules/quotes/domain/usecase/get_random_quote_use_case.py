from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import (
    QuoteRepositoryInterface,
)


class GetRandomQuoteUseCase:
    def __init__(self, quote_repository: QuoteRepositoryInterface):
        self.quote_repository = quote_repository

    async def execute(self) -> Quote | None:
        quote = await self.quote_repository.get_random_quote()
        return quote
