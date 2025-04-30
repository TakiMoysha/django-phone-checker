import logging
import os
from typing import override

from django.core.files.storage import FileSystemStorage
from django.core.files.storage.base import Storage
from django.db import models

from phones.lib.validators import validate_phone_rus

# ====================================================================

logger = logging.getLogger(__name__)

# ====================================================================

registry_files_storage = FileSystemStorage(location="tmp/registry")

# ====================================================================


class DEFPhone(models.Model):
    avs = models.IntegerField()
    start = models.IntegerField()
    to = models.IntegerField()
    capacity = models.IntegerField()
    operator = models.TextField()
    region = models.CharField(max_length=255)
    territory = models.CharField(max_length=255)
    inn = models.CharField(max_length=255)

    @override
    def __str__(self) -> str:
        return f"DEFPhone<{self.avs};{self.start};{self.to};{self.capacity};{self.operator};{self.region};{self.territory};{self.inn}>"

    class Meta:
        verbose_name = "DEFPhone"
        verbose_name_plural = "DEFPhones"
        ordering = ["-avs"]


class PhoneNumber(models.Model):
    phone_number = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        validators=[validate_phone_rus],
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


class RegistryFile(models.Model):
    file = models.FileField(
        storage=registry_files_storage,
        blank=False,
        null=False,
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-datetime"]

    @classmethod
    def get_file_storage(cls) -> Storage:
        return cls().file.storage

    @override
    def __str__(self) -> str:
        return f"RegistryFile<{self.file},{self.datetime.strftime('%d.%m.%Y %H:%M')}>"

    def delete(self, *args, **kwargs):
        logger.info(f"Deleting file: {self.file}")
        os.rename(self.file.path, f"{self.file.path}.del")
        super().delete(*args, **kwargs)
