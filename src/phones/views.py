from datetime import datetime
from django.shortcuts import render


def index(request):
    return render(
        request,
        "index.html",
        context={
            "last_updated_timestamp": datetime.now(),
            "server_status": "OK",
        },
    )
