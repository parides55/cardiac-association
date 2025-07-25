from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("heart_disease_info/", views.MoreInfo, name="heart_disease_info"),
    path("become_member/", views.become_member, name="become_member"),
    path("membership_success/<str:orderId>/", views.membership_success, name="membership_success"),
    path("membership_failed/<str:orderId>/", views.membership_failed, name="membership_failed"),
    path("cancel_membership/", views.cancel_membership, name="cancel_membership"),
    path("cancel_monthly_donation/", views.cancel_monthly_donation, name="cancel_monthly_donation")
]