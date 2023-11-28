from __future__ import absolute_import, unicode_literals

from celery import Celery
from celery.schedules import crontab

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "unblock-pages": {
        "task": "innotter.tasks.unblock_pages",
        "schedule": crontab(hour=9, minute=0),
    },
}
