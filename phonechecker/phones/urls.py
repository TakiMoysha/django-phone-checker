from django.urls import path, re_path
from django.shortcuts import redirect

from phones.views import index
from phones.api.views import api_app


def redirect_to_index(request):
    return redirect("index")


urlpatterns = [
    path("", index, name="index"),
    path("api/", api_app.urls, name="api"),
    re_path(r"^.*$", redirect_to_index, name="redirect"),
]
