from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db

v1_router = APIRouter(prefix="/v1")

@v1_router.get("/")
async def v1_hello_world(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    print(f"db is {db}")
    return {"route": "v1"}
