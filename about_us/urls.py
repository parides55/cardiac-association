from django.urls import path
from . import views

urlpatterns = [
    path("people/", views.our_people, name="our_people"),
    path("history/", views.our_history, name="our_history"),
]