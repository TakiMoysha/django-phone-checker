from django.urls import path
from phones.views import index, api

urlpatterns = [
    path("", index, name="index"),
    path("api/", api.urls, name="api"),
]
