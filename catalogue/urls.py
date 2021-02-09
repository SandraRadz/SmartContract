from django.urls import path

from catalogue.views import home

urlpatterns = [
    path("", home, name="homepage")
]
