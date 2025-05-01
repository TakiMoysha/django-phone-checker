import random
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phones.settings")

from django.conf import settings

app = Celery("phones")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


if settings.ENABLE_TELEMETRY:
    rng = random.Random(settings.SECRET_KEY)
    hour = rng.randint(0, 4)
    minute = rng.randint(0, 59)
    app.conf.beat_schedule["send-telemetry-once-a-day"] = {
        "task": "phones.tasks.send_telemetry",
        "schedule": crontab(minute=minute, hour=hour),
    }

app.conf.beat_schedule = {
    "update_local_registry_from_files": {
        "task": "phones.tasks.update_local_registry_from_files",
        "schedule": crontab(minute=random.randint(0, 59)),
    },
}
