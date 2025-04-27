from datetime import datetime
from django.shortcuts import render
from ninja import NinjaAPI, Query, Schema
from ninja.throttling import AnonRateThrottle

from phones.lib.validators import validate_phone_russian
from phones.schemas import PhoneInfoRequestSchema, PhoneInfoResponseSchema


def index(request):
    return render(
        request,
        "index.html",
        context={
            "last_updated_timestamp": datetime.now(),
            "server_status": "OK",
        },
    )


api = NinjaAPI(
    version="1.0",
    title="Phone Checker API",
    throttle=AnonRateThrottle(rate="1/s"),
)


@api.post("/phone/search", response=PhoneInfoResponseSchema)
async def search_phone_number(request, data: PhoneInfoRequestSchema):
    return PhoneInfoResponseSchema(
        phone="",
        operator="MTS",
        region="Russia",
        last_updated="",
    )
