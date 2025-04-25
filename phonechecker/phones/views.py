from django.shortcuts import render
from ninja import Field, NinjaAPI, Query, Schema


def index(request):
    return render(request, "phones/index.html")


api = NinjaAPI(version="1.0")


@api.get("/search")
async def check_phone(request, phone: str = Query[...]):
    try:
        validate_phone(phone)
    except ValidationError as err:
        return {"error": str(err)}

    return {"phone": phone}
