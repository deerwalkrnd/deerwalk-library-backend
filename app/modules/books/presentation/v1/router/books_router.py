from fastapi import APIRouter

from app.modules.books.presentation.v1.controllers.book_controller import BookController

router = APIRouter(prefix="/books", tags=["Books"])

book_controller = BookController()

router.add_api_route(
    path="/",
    endpoint=book_controller.list_books,
    methods=["GET"],
    description="This method is used to get all books.",
    status_code=200,
)

router.add_api_route(
    path="/",
    endpoint=book_controller.create_book,
    methods=["POST"],
    description="This method is used to create a book.",
    status_code=201,
)

router.add_api_route(
    path="/{id}",
    endpoint=book_controller.update_book,
    methods=["PUT"],
    description="This method is used to update a book.",
    status_code=200,
)

router.add_api_route(
    path="/{id}",
    endpoint=book_controller.delete_book,
    methods=["DELETE"],
    description="This method is used to delete a book",
    status_code=204,
)

router.add_api_route(
    path="{id}/genres",
    endpoint=book_controller.get_genres_by_book_id,
    methods=["GET"],
    description="Returns the genres of a book provided in the id field",
    status_code=200,
)
