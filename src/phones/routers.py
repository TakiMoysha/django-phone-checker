from logging import getLogger
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.throttling import AnonRateThrottle

from phones.lib.exceptions import parse_pydantic_error
from phones.schemas import (
    ErrorResponseSchema,
)

from .api import phones_router

logger = getLogger(__file__)


api_app = NinjaAPI(
    version="1.0",
    title="Phone Checker API",
    throttle=AnonRateThrottle(rate="10/s"),
)


@api_app.exception_handler(Exception)
def unexpected_error(request, exception: Exception):
    logger.error("Unexpected error", exc_info=exception)
    return api_app.create_response(
        request,
        ErrorResponseSchema(error=500, details="Something went wrong"),
        status=500,
    )


@api_app.exception_handler(ValidationError)
def validation_error(request, exception: ValidationError):
    return api_app.create_response(
        request,
        ErrorResponseSchema(error=400, details=parse_pydantic_error(exception)),
        status=400,
    )


api_app.add_router(r"phones", phones_router)
