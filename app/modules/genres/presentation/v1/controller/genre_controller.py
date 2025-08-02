from fastapi import Depends
from fastapi import logger
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.genres.domain.entity.genre import Genre
from app.modules.genres.domain.request.genre_create_request import CreateGenreReqeust
from app.modules.genres.domain.request.genre_list_params import GenreListParams
from app.core.dependencies.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.genres.domain.request.genre_update_request import GenreUpdateRequest
from app.modules.genres.domain.usecase.create_genre_use_case import CreateGenreUseCase
from app.modules.genres.domain.usecase.delete_genre_by_id_use_case import (
    DeleteGenreByIdUseCase,
)
from app.modules.genres.domain.usecase.get_many_genre_use_case import (
    GetManyGenreUseCase,
)
from app.modules.genres.domain.usecase.get_genre_by_id_use_case import (
    GetGenreByIdUseCase,
)
from app.modules.genres.domain.usecase.update_genre_by_id_use_case import (
    UpdateGenreByIdUseCase,
)
from app.modules.genres.infra.genre_repository import GenreRepository


class GenreController:
    def __init__(self) -> None:
        pass

    async def list_genre(
        self, params: GenreListParams = Depends(), db: AsyncSession = Depends(get_db)
    ) -> PaginatedResponseMany[Genre] | None:
        genre_repository = GenreRepository(db=db)

        try:
            get_many_genre_use_case = GetManyGenreUseCase(
                genre_repository=genre_repository
            )

            genres = await get_many_genre_use_case.execute(
                page=params.page,
                limit=params.limit,
                searchable_value=params.searchable_value,
                searchable_field=params.searchable_field,
                starts=params.starts,
                ends=params.ends,
            )

            return PaginatedResponseMany(
                page=params.page,
                total=len(genres),
                next=params.page + 1,
                items=genres,
            )

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not fetch genres",
            )

    async def create_genre(
        self,
        create_genre_request: CreateGenreReqeust,
        db: AsyncSession = Depends(get_db),
    ) -> Genre | None:
        genre_repository = GenreRepository(db=db)

        try:
            create_genre_use_case = CreateGenreUseCase(
                genre_repository=genre_repository
            )

            genre = await create_genre_use_case.execute(
                title=create_genre_request.title,
                image_url=create_genre_request.image_url,
            )

            return genre

        except ValueError as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="quote already exists",
            )

    async def update_genre(
        self,
        id: int,
        genre_update_request: GenreUpdateRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        genre_repository = GenreRepository(db=db)

        get_genre_by_id_use_case = GetGenreByIdUseCase(
            genre_repository=genre_repository
        )

        genre = await get_genre_by_id_use_case.execute(id=id)

        if not genre:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="genre you're deleting does not exist",
            )

        update_genre_by_id_use_case = UpdateGenreByIdUseCase(
            genre_repostory=genre_repository
        )

        await update_genre_by_id_use_case.execute(
            conditions=Genre(id=id),
            new=Genre(**genre_update_request.model_dump(exclude_unset=True)),
        )

        return None

    async def delete_genre(self, id: int, db: AsyncSession = Depends(get_db)) -> None:
        genre_repository = GenreRepository(db=db)

        get_genre_by_id_use_case = GetGenreByIdUseCase(
            genre_repository=genre_repository
        )

        genre = await get_genre_by_id_use_case.execute(id=id)

        if not genre:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="genre that your'e trying to delete does not exist.",
            )

        delete_genre_by_id_use_case = DeleteGenreByIdUseCase(
            genre_repository=GenreRepository(db=db)
        )

        await delete_genre_by_id_use_case.execute(id=id)
