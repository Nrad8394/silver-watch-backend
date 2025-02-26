import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silver_watch.settings")

celery_app = Celery("silver_watch")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.update(
    broker_connection_retry_on_startup=True,  # ✅ Fix deprecation warning
)

@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
