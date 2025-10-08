from app.modules.book_borrow.domain.request.book_borrow_request import BookBorrowRequest


class BookBorrowController:
    def __init__(self) -> None:
        pass

    async def borrow_book(self, book_borrow_request: BookBorrowRequest):
        raise NotImplementedError
