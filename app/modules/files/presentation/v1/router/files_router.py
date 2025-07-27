from fastapi import APIRouter

from app.modules.files.presentation.v1.controller.file_controller import FileController

router = APIRouter(prefix="/files", tags=["utils", "files"])
file_controller = FileController()

router.add_api_route("/upload", endpoint=file_controller.upload, methods=["POST"])
