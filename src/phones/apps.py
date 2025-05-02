import logging
from typing import override

from django.apps import AppConfig

logger = logging.getLogger(__name__)


def registrate_tasks() -> None:
    """create background models and scheduler for background tasks"""
    from background_task.tasks import tasks

    tasks.background(
        name="update_local_registry",
        remove_existing_tasks=True,
    )


def connect_phones_signals() -> None:
    from background_task.models import CompletedTask
    from phones.signals import *
    # TODO: connect CompletedTask("update_registry") and `REFRESH MATERIALIZE VIEW phones_defphone`



class PhonesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "phones"

    @override
    def ready(self):
        registrate_tasks()
        connect_phones_signals()
