from django.shortcuts import render
from ninja import NinjaAPI, Query
from ninja.throttling import AnonRateThrottle

from phones.schemas import PhoneInfoResponseSchema


def index(request):
    return render(request, "index.html")


api = NinjaAPI(
    version="1.0",
    title="Phone Checker API",
    throttle=AnonRateThrottle(rate="1/s"),
)


@api.post("/phone/search", response=PhoneInfoResponseSchema)
async def search_phone_number(request, phone: Query[str]):
    return PhoneInfoResponseSchema(phone=phone, operator="MTS", region="Russia")
