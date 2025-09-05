from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.books.domain.entities.books_genre import BooksGenre


class BooksGenreRepositoryInterface(RepositoryInterface[BooksGenre]):
    pass
