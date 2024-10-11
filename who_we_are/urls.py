from django.urls import path
from . import views

urlpatterns = [
    path("", views.who_we_are, name="who_we_are"),
]