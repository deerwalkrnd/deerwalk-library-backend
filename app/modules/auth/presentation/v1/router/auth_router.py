from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.get("/")
async def auth():
    return "auth-route"

