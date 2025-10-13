from abc import abstractmethod
from typing import List

from app.core.domain.repositories.repository_interface import \
    RepositoryInterface
from app.modules.books.domain.entities.books_genre import BooksGenre
from app.modules.genres.domain.entity.genre import Genre


class BooksGenreRepositoryInterface(RepositoryInterface[BooksGenre]):
    @abstractmethod
    async def get_genres_by_book_id(self, book_id: int) -> List[Genre]:
        raise NotImplementedError

    pass
