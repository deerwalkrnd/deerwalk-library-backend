from pathlib import Path

from fastapi import FastAPI, Request, logger
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.dependencies.get_settings import get_settings
from app.core.exc.error_code import ErrorCode
from app.routers.v1.router import v1_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Deerwalk Library Backend API",
    description="The API built for Deerwalk College's Library System. Open Souce and built for all libraries across Nepal",
    redirect_slashes=False,
)

app.include_router(v1_router)

# Serve locally-stored uploads (book covers, profile images, event banners).
_media_dir = Path(get_settings().upload_dir)
_media_dir.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(_media_dir)), name="media")



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dss-library.deerwalk.edu.np",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# for missing fields
@app.exception_handler(exc_class_or_status_code=RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.logger.error(exc)
    return JSONResponse(
        content={
            "detail": {
                "code": ErrorCode.INVALID_FIELDS,
                "msg": "Some of the fields are incorrectly filled.",
                "fields": exc.errors(),
            }
        },
        status_code=400,
    )


@app.get("/")
async def hello_world() -> dict[str, str]:
    return {"mesasge": "hello World"}
