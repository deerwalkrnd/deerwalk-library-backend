from app.core.domain.repositories.repository_interface import \
    RepositoryInterface
from app.modules.books.domain.entities.book_copy import BookCopy


class BookCopyRepositoryInterface(RepositoryInterface[BookCopy]):
    pass
