from fastapi import APIRouter

from app.modules.teacher_recommendations.presentation.v1.controllers.teacher_recommendation_controller import (
    TeacherRecommendationController,
)

router = APIRouter(prefix="/teacher-recommendations", tags=["teacher-recommendations"])

teacher_recommendation_controller = TeacherRecommendationController()

router.add_api_route(
    path="/",
    endpoint=teacher_recommendation_controller.list_teacher_recommendations,
    methods=["GET"],
    description="This method is used to get all teacher recommendations.",
    status_code=200,
)
router.add_api_route(
    path="/",
    endpoint=teacher_recommendation_controller.create_teacher_recommendation,
    methods=["POST"],
    description="This method is used to create a teacher recommendation.",
    status_code=201,
)
router.add_api_route(
    path="/{id}",
    endpoint=teacher_recommendation_controller.update_teacher_recommendation,
    methods=["PUT"],
    description="This method is used to update a teacher recommendation.",
    status_code=200,
)
router.add_api_route(
    path="/{id}",
    endpoint=teacher_recommendation_controller.delete_teacher_recommendation,
    methods=["DELETE"],
    description="This method is used to delete a teacher recommendation",
    status_code=204,
)
