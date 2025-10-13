from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import \
    QuoteRepositoryInterface


class GetQuoteByIdUseCase:
    def __init__(self, quote_repository: QuoteRepositoryInterface) -> None:
        self.quote_repository = quote_repository

    async def execute(self, id: int) -> Quote | None:
        return await self.quote_repository.find_one(obj=Quote(id=id))
