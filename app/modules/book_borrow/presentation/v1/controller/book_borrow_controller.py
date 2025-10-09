from typing import Any
from app.modules.book_borrow.domain.request.book_borrow_request import BookBorrowRequest


class BookBorrowController:
    def __init__(self) -> None:
        pass

    async def borrow_book(self, book_borrow_request: BookBorrowRequest) -> None:
        raise NotImplementedError

    async def renew_book(self, book_renew_request: Any) -> None:
        raise NotImplementedError

    async def return_book(self, return_book_request: Any) -> None:
        raise NotImplementedError
