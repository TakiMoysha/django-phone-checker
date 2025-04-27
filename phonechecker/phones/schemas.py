from dataclasses import dataclass
from ninja import Schema


class PhoneInfoRequestSchema(Schema):
    phone: str
    email: str | None


class PhoneInfoResponseSchema(Schema):
    phone: str
    operator: str
    region: str
    last_updated: str


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
