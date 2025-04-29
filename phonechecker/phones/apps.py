import logging
from typing import override

from django.apps import AppConfig

logger = logging.getLogger(__name__)


def registrate_tasks() -> None:
    """Loaded tasks and depenencies and (re)create apropriate models."""
    from phones.tasks import update_database_from_registry
    from background_task.tasks import tasks, Task

    tasks.background(update_database_from_registry, remove_existing_tasks=True)


class PhonesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    events = []
    name = "phones"

    @override
    def ready(self):
        registrate_tasks()
        return super().ready()
