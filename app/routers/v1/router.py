from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.modules.auth.presentation.v1.router.auth_router import router as auth_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)

@v1_router.get("/")
async def v1_hello_world(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    print(f"db is {db}")
    return {"route": "v1"}
