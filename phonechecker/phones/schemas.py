import logging
from dataclasses import dataclass
from typing import Annotated

from ninja import Schema
from pydantic import AfterValidator, BeforeValidator, field_validator

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


@dataclass(slots=True, frozen=True)
class DefPhoneSchema:
    avs: int
    from_: int
    to: int
    capacity: int
    operator: str
    region: str
    territory: str
    inn: str
