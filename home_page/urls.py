from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("heart_disease_info/", views.MoreInfo, name="heart_disease_info"),
    path("become_member/", views.Become_member, name="become_member"),
    path("donations/", views.Donations, name="donations"),
]