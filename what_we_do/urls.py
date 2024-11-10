from django.urls import path
from . import views

urlpatterns = [
    path("", views.WhatWeDo, name="what_we_do"),
]