from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")


@v1_router.get("/")
async def v1_hello_world() -> dict[str, str]:
    return {"route": "v1"}
