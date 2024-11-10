from django.urls import path
from . import views

urlpatterns = [
    path("", views.HowYouCanHelp, name="how_you_can_help"),
]