from django.db import models


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=20, blank=False, null=False)


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
