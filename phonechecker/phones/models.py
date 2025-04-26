import logging
from typing import override
from django.db import models

from phones.lib.validators import validate_phone_russian

logger = logging.getLogger(__name__)


class PhoneNumber(models.Model):
    phone_number = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        validators=[validate_phone_russian],
    )

    @override
    def __str__(self) -> str:
        return f"PhoneNumber<{self.phone_number}>"


class EventLog(models.Model):
    datetime = models.DateTimeField(
        verbose_name="Datetime of action",
        auto_now_add=True,
    )
    action = models.CharField(
        verbose_name="What the action",
        max_length=255,
    )
    log = models.TextField(
        verbose_name="Result of action",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-datetime"]

    @override
    def __str__(self) -> str:
        return f"EventLog<{self.action}:{self.datetime.strftime('%d.%m.%Y %H:%M')}>"
