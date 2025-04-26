import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class PhonesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    events = []
    name = "phones"

    def ready(self):
        # from .containers import UserPhoneContainer

        # user_phone_container = UserPhoneContainer()
        # user_phone_container.wire(modules=["phones"])
        #
        # event_log_container = EventLogContainer()
        # event_log_container.wire(modules=["phones"])

        logger.info("Ready")

        return super().ready()
