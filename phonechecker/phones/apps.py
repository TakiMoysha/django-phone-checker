import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class PhonesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    events = []
    name = "phones"

    def ready(self):
        return super().ready()
