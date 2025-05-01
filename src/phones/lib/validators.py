import logging
from typing import Any, Callable

from django.core.exceptions import ValidationError as DjValidationError

import phonenumbers
from pydantic import ValidatorFunctionWrapHandler


logger = logging.getLogger(__name__)


def validate_phone_rus(value: Any) -> tuple[bool, str | None]:
    logger.debug("Validating phone number: %s", value)
    try:
        number = phonenumbers.parse(value, "RU")
    except phonenumbers.NumberParseException as err:
        logger.debug("Error parsing phone number: %s", err)
        return (False, "Invalid phone number or unsupported country")

    if not phonenumbers.is_valid_number_for_region(number, "RU"):
        logger.debug("Phone number is not valid for Russia")
        return (False, "Invalid phone number or unsupported country")

    logger.debug("Phone number parsed: %s", number)
    return (value, None)


def model_validate_phone_rus(value: str) -> str:
    (is_valid, error) = validate_phone_rus(value)

    if not is_valid:
        raise DjValidationError(error or "Invalid phone number")

    return value
