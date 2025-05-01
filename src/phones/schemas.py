import logging
from dataclasses import dataclass
from typing import Annotated

from ninja import Schema
from pydantic import BeforeValidator, Field, field_validator, EmailStr

from phones.lib.sanitizers import sanitize_phone
from phones.lib.validators import validate_phone_rus
from phones.models import DEFPhone

logger = logging.getLogger(__name__)


class PhoneInfoRequestSchema(Schema):
    phone: Annotated[str, BeforeValidator(sanitize_phone)]
    email: EmailStr | None

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        (is_valid, reason) = validate_phone_rus(value)
        if not is_valid:
            raise ValueError(reason)
        return value


class PhoneInfoResponseSchema(Schema):
    phone: str
    operator: str
    region: str
    last_updated: str


class ErrorResponseSchema(Schema):
    error: int
    details: str | dict
