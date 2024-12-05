from django.urls import path
from . import views

urlpatterns = [
    path("donations/", views.donations, name="donations"),
    path("online_shop/", views.online_shop, name="online_shop"),
    path("basket/", views.view_basket, name="basket"),
    path("add_to_basket/<int:product_id>/", views.add_to_basket, name="add_to_basket"),
    path("basket/remove_from_basket/<int:product_id>/", views.remove_from_basket, name="remove_from_basket"),
    path("donation_checkout/", views.donation_checkout, name="donation_checkout"),
    path("basket_checkout/", views.basket_checkout, name="basket_checkout"),
]