from django.urls import path
from . import views

urlpatterns = [
    path("donations/", views.donations, name="donations"),
    path("online_shop/", views.online_shop, name="online_shop"),
    path("basket/", views.view_basket, name="basket"),
    path("add_to_basket/<int:product_id>/", views.add_to_basket, name="add_to_basket"),
]