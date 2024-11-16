from django.urls import path
from . import views

urlpatterns = [
    path("", views.News.as_view(), name="news"),
    path("<slug:slug>/", views.new_detail, name="new_detail"),
]