from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.modules.auth.presentation.v1.router.auth_router import router as auth_router
from app.modules.books.presentation.v1.router.books_router import router as books_router
from app.modules.events.presentation.v1.router.events_router import (
    router as event_router,
)
from app.modules.feedbacks.presentation.v1.router.feedback_router import (
    router as feedbacks_router,
)
from app.modules.files.presentation.v1.router.files_router import router as files_router
from app.modules.genres.presentation.v1.router.genre_router import (
    router as genre_router,
)
from app.modules.quotes.presentation.v1.router.quotes_router import (
    router as quotes_router,
)
from app.modules.recommendations.presentation.v1.router.recommendation_router import (
    router as recommendation_router,
)

from app.modules.users.presentation.v1.router.users_router import router as users_router
from app.modules.bookmarks.presentation.v1.router.bookmark_router import (
    router as bookmark_router,
)
from app.modules.books_reviews.presentation.v1.router.books_reviews_router import (
    router as books_reviews_router,
)
from app.modules.books_reviews.presentation.v1.router.books_reviews_router import (
    router as books_reviews_router,
)

from app.modules.book_borrow.presentation.v1.router.book_borrow_router import router as book_borrow_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(books_router)
v1_router.include_router(users_router)
v1_router.include_router(files_router)
v1_router.include_router(quotes_router)
v1_router.include_router(feedbacks_router)
v1_router.include_router(genre_router)
v1_router.include_router(event_router)
v1_router.include_router(recommendation_router)
v1_router.include_router(bookmark_router)
v1_router.include_router(books_reviews_router)
v1_router.include_router(book_borrow_router)


# remove at production
@v1_router.get("/")
async def v1_hello_world(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    print(f"db is {db}")
    return {"route": "v1"}
