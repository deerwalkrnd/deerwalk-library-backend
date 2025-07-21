from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from app.core.dependencies.get_settings import get_settings
from ..models import Base

settings = get_settings()
engine : AsyncEngine = create_async_engine(url=settings.database_url)
SessionLocal = async_sessionmaker(bind=engine)

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    db = SessionLocal()

    try:
        yield db 
    finally: 
        await db.close()

