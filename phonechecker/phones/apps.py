import logging
from typing import override

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class PhonesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    events = []
    name = "phones"

    @override
    def ready(self):
        # from phones.tasks import update_database_from_registry
        #
        # update_database_from_registry()
        return super().ready()
