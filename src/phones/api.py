from logging import getLogger
from ninja import Router

from phones.schemas import (
    ErrorResponseSchema,
    PhoneInfoRequestSchema,
    PhoneInfoResponseSchema,
)
from phones.services import find_def_phone_by_number

logger = getLogger(__file__)

phones_router = Router()


@phones_router.post(
    "/search",
    response={200: PhoneInfoResponseSchema, 400: ErrorResponseSchema},
)
async def search_phone_number(request, data: PhoneInfoRequestSchema):
    result = find_def_phone_by_number(data)
    return 200, PhoneInfoResponseSchema(
        phone="",
        operator="",
        region="",
        last_updated="",
    )
