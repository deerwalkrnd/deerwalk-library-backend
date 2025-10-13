from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.repositories.quote_repository_interface import \
    QuoteRepositoryInterface


class CreateQuoteUseCase:
    def __init__(self, quote_repository: QuoteRepositoryInterface) -> None:
        self.quote_repository = quote_repository

    async def execute(self, author: str, quote: str) -> Quote | None:
        already = await self.quote_repository.find_one(
            obj=Quote(author=author, quote=quote)
        )

        if already:
            raise ValueError("quote already exists")

        return await self.quote_repository.create(obj=Quote(author=author, quote=quote))
