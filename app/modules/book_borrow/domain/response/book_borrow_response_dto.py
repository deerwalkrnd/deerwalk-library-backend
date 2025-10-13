from app.modules.book_borrow.domain.entities.book_borrow import BookBorrow


class BookBorrowResponseDTO(BookBorrow):
    class Config:
        from_attributes = True
