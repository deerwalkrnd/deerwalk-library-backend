from fastapi import APIRouter

from app.modules.book_copies.presentation.v1.controller.book_copy_controller import (
    BookCopyController,
)


router = APIRouter(prefix="/book-copy", tags=["book copy"])
book_copy_controller = BookCopyController()

router.add_api_route(
    path="/",
    endpoint=book_copy_controller.get_available_book_copies,
    methods=["GET"],
    response_description="Returns availabe book copies",
)
