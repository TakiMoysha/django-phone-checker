from logging import getLogger
from django.db.models.signals import post_save
from django.dispatch import receiver

from phones.models import PhoneNumber

logger = getLogger(__name__)


@receiver(post_save, sender=PhoneNumber)
def new_number_handler(sender, instance, **kwargs):
    logger.info(f"New number: {instance}")
