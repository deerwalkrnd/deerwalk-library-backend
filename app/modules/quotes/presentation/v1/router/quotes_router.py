from fastapi import APIRouter

from app.modules.quotes.presentation.v1.controllers.quotes_controller import \
    QuotesController

router = APIRouter(prefix="/quotes", tags=["quotes"])

quotes_controller = QuotesController()

router.add_api_route(
    path="/",
    endpoint=quotes_controller.list_quotes,
    methods=["GET"],
    description="This method",
)

router.add_api_route(
    path="/",
    endpoint=quotes_controller.create_quote,
    methods=["POST"],
)

router.add_api_route(
    path="/{id}",
    methods=["PUT"],
    endpoint=quotes_controller.update_quote,
    description="Update a quote",
)

router.add_api_route(
    path="/{id}",
    methods=["DELETE"],
    endpoint=quotes_controller.delete_quote,
    description="Delete a quote",
)

router.add_api_route(
    path="/random-quote",
    methods=["GET"],
    endpoint=quotes_controller.get_random_quote,
    description="returns a random quote.",
)
