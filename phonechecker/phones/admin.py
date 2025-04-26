from django.contrib import admin

from .models import EventLog, PhoneNumber


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin): ...


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin): ...
