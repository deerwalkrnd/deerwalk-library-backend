from fastapi import FastAPI

from app.routers.v1.router import v1_router

app = FastAPI(
    title="Deerwalk Library Backend API",
)

app.include_router(v1_router)


@app.get("/")
async def hello_world() -> dict[str, str]:
    return {"mesasge": "hello World"}
