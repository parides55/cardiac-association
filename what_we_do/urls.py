from django.urls import path
from . import views

urlpatterns = [
    path("", views.WhatWeDo, name="what_we_do"),
    path("services/", views.Services, name="services"),
    path("programs/", views.Programs, name="programs"),
]