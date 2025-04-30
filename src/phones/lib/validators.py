import logging
from typing import Any

import phonenumbers
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


def validate_phone_rus(value: Any):
    logger.debug("Validating phone number: %s", value)
    try:
        number = phonenumbers.parse(value, "RU")
    except Exception as err:
        logger.debug("Error parsing phone number: %s", err)
        raise ValidationError("Invalid phone number or unsupported country")

    if not phonenumbers.is_valid_number_for_region(number, "RU"):
        logger.debug("Phone number is not valid for Russia")
        raise ValidationError("Invalid phone number or unsupported country")

    logger.debug("Phone number parsed: %s", number)
    return value
