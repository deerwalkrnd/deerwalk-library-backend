from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow


class BookBorrowRepositoryInterface(RepositoryInterface[BookBorrow]):
    pass
