from django.contrib import admin

from .models import EventLog, PhoneNumber, RegistryFile


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin): ...


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin): ...


@admin.register(RegistryFile)
class RegistryFileAdmin(admin.ModelAdmin): ...
