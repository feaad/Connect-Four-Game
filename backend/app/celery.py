import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.log.setup()

app.conf.beat_schedule = {
    "process-matchmaking": {
        "task": "game.tasks.process_matchmaking",
        "schedule": crontab(minute="*/1"),
    },
}
