from fastapi import Depends
from fastapi import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.quotes.domain.entities.quote import Quote
from app.modules.quotes.domain.request.quote_create_request import QuoteCreateRequest
from app.modules.quotes.domain.request.quote_list_params import QuoteListParams
from app.modules.quotes.domain.request.quote_update_request import QuoteUpdateRequest
from app.modules.quotes.domain.usecase.create_quote_use_case import CreateQuoteUseCase
from app.modules.quotes.domain.usecase.delete_quote_by_id_use_case import (
    DeleteQuoteByIdUseCase,
)
from app.modules.quotes.domain.usecase.get_many_quotes_use_case import (
    GetManyQuotesUseCase,
)
from app.modules.quotes.domain.usecase.get_quote_by_id_use_case import (
    GetQuoteByIdUseCase,
)
from app.modules.quotes.domain.usecase.get_random_quote_use_case import (
    GetRandomQuoteUseCase,
)
from app.modules.quotes.domain.usecase.update_quote_by_id_use_case import (
    UpdateQuoteByIdUseCase,
)
from app.modules.quotes.infra.repositories.quote_repository import QuoteRepository


class QuotesController:
    def __init__(self) -> None:
        pass

    async def list_quotes(
        self, params: QuoteListParams = Depends(), db: AsyncSession = Depends(get_db)
    ) -> PaginatedResponseMany[Quote]:
        quote_repository = QuoteRepository(db=db)

        try:
            get_many_quotes_use_case = GetManyQuotesUseCase(
                quote_repository=quote_repository
            )
            quotes = await get_many_quotes_use_case.execute(
                page=params.page,
                limit=params.limit,
                searchable_field=params.searchable_field,
                searchable_value=params.searchable_value,
                ends=params.ends,
                starts=params.starts,
            )
            return PaginatedResponseMany(
                page=params.page, total=len(quotes), next=params.page + 1, items=quotes
            )
        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not fetch quotes",
            )

    async def create_quote(
        self,
        quote_create_request: QuoteCreateRequest,
        db: AsyncSession = Depends(get_db),
    ) -> Quote | None:
        quote_repository = QuoteRepository(db=db)

        try:
            create_quote_use_case = CreateQuoteUseCase(
                quote_repository=quote_repository
            )
            new_quote = await create_quote_use_case.execute(
                quote_create_request.author, quote=quote_create_request.quote
            )
            return new_quote
        except ValueError as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="quote already exists",
            )

    async def update_quote(
        self,
        id: int,
        quote_update_request: QuoteUpdateRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        quote_repository = QuoteRepository(db)
        get_quote_by_id_use_case = GetQuoteByIdUseCase(
            quote_repository=quote_repository
        )

        quote = await get_quote_by_id_use_case.execute(id=id)

        if not quote:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="quote you're deleting does not exist",
            )
        update_quote_by_id_use_case = UpdateQuoteByIdUseCase(
            quote_repostitory=quote_repository
        )

        await update_quote_by_id_use_case.execute(
            conditions=Quote(id=id),
            new=Quote(**quote_update_request.model_dump(exclude_unset=True)),
        )

        return None

    async def delete_quote(self, id: int, db: AsyncSession = Depends(get_db)) -> None:
        quote_repository = QuoteRepository(db=db)

        get_quote_by_id_use_case = GetQuoteByIdUseCase(
            quote_repository=quote_repository
        )

        quote = await get_quote_by_id_use_case.execute(id=id)

        if not quote:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="quote you're deleting does not exist",
            )
        delete_quote_by_id_use_case = DeleteQuoteByIdUseCase(
            quote_repository=quote_repository
        )
        return await delete_quote_by_id_use_case.execute(id=id)

    async def get_random_quote(self, db: AsyncSession = Depends(get_db)) -> Quote:
        quote_repository = QuoteRepository(db=db)

        get_random_quote_use_case = GetRandomQuoteUseCase(
            quote_repository=quote_repository
        )

        quote = await get_random_quote_use_case.execute()

        if not quote:
            raise LibraryException(
                status_code=404, code=ErrorCode.NOT_FOUND, msg="no quotes found."
            )

        return quote
