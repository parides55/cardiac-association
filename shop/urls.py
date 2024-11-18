from django.urls import path
from . import views

urlpatterns = [
    path("donations/", views.Donations, name="donations"),
    path("online_shop/", views.OnlineShop, name="online_shop"),
]