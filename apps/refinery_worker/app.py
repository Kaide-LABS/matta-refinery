from celery import Celery
from apps.refinery_api.config import settings

app = Celery("refinery")
app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    broker_url=settings.celery_broker,
    broker_transport_options={"visibility_timeout": 3600},
    task_serializer="json",
    result_backend=settings.redis_url,
)

app.autodiscover_tasks(["apps.refinery_worker.tasks"])
