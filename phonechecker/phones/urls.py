from django.urls import path, re_path
from phones.views import index, api
from django.shortcuts import redirect


def redirect_to_index(request):
    return redirect("index")


urlpatterns = [
    path("", index, name="index"),
    path("api/", api.urls, name="api"),
    re_path(r"^.*$", redirect_to_index, name="redirect"),
]
