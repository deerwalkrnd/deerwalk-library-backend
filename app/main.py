from fastapi import FastAPI, Request, logger
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exc.error_code import ErrorCode
from app.routers.v1.router import v1_router

app = FastAPI(
    title="Deerwalk Library Backend API",
)

app.include_router(v1_router)

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
