from django.urls import path
from . import views

urlpatterns = [
    path("", views.events, name="events"),
    path('<slug:slug>/', views.event_info, name='event_info'),
]