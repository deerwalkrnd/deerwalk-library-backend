from fastapi import APIRouter

from app.modules.book_borrow.presentation.v1.controller.book_borrow_controller import (
    BookBorrowController,
)

router = APIRouter(prefix="/book-borrow")
book_borrow_controller = BookBorrowController()

router.add_api_route(
    "/{book_copy_id}",
    methods=["POST"],
    endpoint=book_borrow_controller.borrow_book,
    response_description="Returns the book borrowed entity",
)
