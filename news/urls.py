from django.urls import path
from . import views

urlpatterns = [
    path("", views.News.as_view(), name="news"),
]