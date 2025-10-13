from app.core.domain.repositories.repository_interface import \
    RepositoryInterface
from app.modules.books.domain.entities.book import Book


class BookRepositoryInterface(RepositoryInterface[Book]):
    pass
