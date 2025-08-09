from fastapi import APIRouter

from app.modules.genres.presentation.v1.controller.genre_controller import (
    GenreController,
)


router = APIRouter(prefix="/genre", tags=["genre"])

genre_controller = GenreController()


router.add_api_route(
    path="/",
    endpoint=genre_controller.list_genre,
    methods=["GET"],
    description="This route gets all genre",
)


router.add_api_route(
    path="/",
    methods=["POST"],
    endpoint=genre_controller.create_genre,
    description="This route creates genres",
)

router.add_api_route(
    path="/{id}",
    methods=["PUT"],
    endpoint=genre_controller.update_genre,
    description="This route updates genre",
)

router.add_api_route(
    path="/{id}",
    methods=["DELETE"],
    endpoint=genre_controller.delete_genre,
    description="This route deletes the genre",
)
