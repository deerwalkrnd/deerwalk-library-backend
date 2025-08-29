from celery import Celery

from app.core.dependencies.get_settings import get_settings

settings = get_settings()

celery_app = Celery(
    "deerwalk-library",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.background.tasks.email_task",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_serializer_kwargs={"ensure_ascii": False},
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

celery_app.autodiscover_tasks()
