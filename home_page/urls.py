from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("heart_disease_info/", views.MoreInfo, name="heart_disease_info"),
    path("become_member/", views.Become_member, name="become_member"),
    path("membership_success/<int:unique_order_number>?<int:orderId>/", views.membership_success, name="membership_success"),
    path("membership_failed/", views.membership_failed, name="membership_failed"),
]