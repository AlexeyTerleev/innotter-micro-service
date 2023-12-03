from datetime import date

from app.celery import app
from innotter.models import Page


@app.task
def unblock_pages():
    Page.objects.filter(blocked=True, unblock_date__lte=date.today()).update(
        blocked=False, unblock_date=None
    )
