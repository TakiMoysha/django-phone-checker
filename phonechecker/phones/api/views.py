from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.throttling import AnonRateThrottle

from phones.schemas import (
    ErrorResponseSchema,
    PhoneInfoRequestSchema,
    PhoneInfoResponseSchema,
)

api_app = NinjaAPI(
    version="1.0",
    title="Phone Checker API",
    throttle=AnonRateThrottle(rate="1/s"),
)


@api_app.exception_handler(Exception)
def unexpected_error(request, exception):
    return api_app.create_response(
        request,
        ErrorResponseSchema(error=500, detail=exception.message),
        status=500,
    )


@api_app.exception_handler(ValidationError)
def validation_error(request, exception):
    return api_app.create_response(
        request,
        ErrorResponseSchema(error=400, detail=exception.message),
        status=400,
    )


@api_app.post(
    "/phones/search",
    response={200: PhoneInfoResponseSchema, 400: ErrorResponseSchema},
)
async def search_phone_number(request, data: PhoneInfoRequestSchema):
    return 200, PhoneInfoResponseSchema(
        phone="",
        operator="MTS",
        region="Russia",
        last_updated="",
    )
