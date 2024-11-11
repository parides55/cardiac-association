from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("heart_disease_info/", views.MoreInfo, name="heart_disease_info"),
]