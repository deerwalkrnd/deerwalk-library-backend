from fastapi import APIRouter

from app.modules.recommendations.presentation.v1.controllers.recommendation_controller import (
    RecommendationController,
)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

recommendation_controller = RecommendationController()

router.add_api_route(
    path="/",
    endpoint=recommendation_controller.list_recommendations,
    methods=["GET"],
    description="This method is used to get all recommendations.",
    status_code=200,
)
router.add_api_route(
    path="/",
    endpoint=recommendation_controller.create_recommendation,
    methods=["POST"],
    description="This method is used to create a recommendation.",
    status_code=201,
)
router.add_api_route(
    path="/{id}",
    endpoint=recommendation_controller.update_recommendation,
    methods=["PUT"],
    description="This method is used to update a recommendation.",
    status_code=200,
)
router.add_api_route(
    path="/{id}",
    endpoint=recommendation_controller.delete_recommendation,
    methods=["DELETE"],
    description="This method is used to delete a recommendation",
    status_code=204,
)

