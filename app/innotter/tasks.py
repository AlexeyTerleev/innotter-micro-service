from datetime import date
from innotter.models import Page
from app.celery import app


@app.task
def unblock_pages():    
    Page.objects.filter(blocked=True, unblock_date__lte=date.today()).update(blocked=False, unblock_date=None)  