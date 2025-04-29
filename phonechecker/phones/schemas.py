import logging
from dataclasses import dataclass

from ninja import Schema
from pydantic import field_validator

from phones.lib.sanitizers import sanitize_phone
from phones.lib.validators import validate_phone_rus

logger = logging.getLogger(__name__)


class PhoneInfoRequestSchema(Schema):
    phone: str
    email: str | None = None

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        value = sanitize_phone(value)
        validate_phone_rus(value)
        return value


class PhoneInfoResponseSchema(Schema):
    phone: str
    operator: str
    region: str
    last_updated: str


class ErrorResponseSchema(Schema):
    error: int
    detail: str

