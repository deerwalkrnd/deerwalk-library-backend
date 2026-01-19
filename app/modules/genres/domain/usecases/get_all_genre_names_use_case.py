from typing import Set

from app.modules.genres.domain.repositories.genre_repository_interface import (
    GenreRepositoryInterface,
)


class GetAllGenreNamesUseCase:
    """Use case to retrieve all genre names from the database."""

    def __init__(self, genre_repository: GenreRepositoryInterface) -> None:
        self.genre_repository = genre_repository

    async def execute(self) -> Set[str]:
        """
        Returns a set of all genre names (titles) in the database.
        """
        # Get all genres with a high limit
        genres = await self.genre_repository.find_many(
            limit=1000,
            offset=0,
            sort_by="title",
            descending=False,
        )
        
        return {genre.title for genre in genres if genre.title}
