from fastapi import APIRouter

from app.modules.books_reviews.presentation.v1.controllers.books_reviews_controller import (
    BooksReviewsController,
)

router = APIRouter(prefix="/reviews", tags=["books-reviews"])

books_reviews_controller = BooksReviewsController()


router.add_api_route(
    path="/count",
    endpoint=books_reviews_controller.count_book_reviews,
    methods=["GET"],
    description="This method is used to count the book reviews by book id.",
    status_code=200,
)
router.add_api_route(
    path="",
    endpoint=books_reviews_controller.get_book_reviews_by_book_id,
    methods=["GET"],
    description="This method is used to get book reviews by book id.",
    status_code=200,
)

router.add_api_route(
    path="",
    endpoint=books_reviews_controller.create_book_review,
    methods=["POST"],
    description="This method is used to create a book review.",
    status_code=201,
)

router.add_api_route(
    path="/{id}",
    endpoint=books_reviews_controller.mark_spam,
    methods=["PUT"],
    description="This method is used to mark a review as spam",
    status_code=200,
)

# is this route necessary tho, cant the frontend just do
# const response = fetch ('/reviews',...)
# const count = response.json().len()
