from django.urls import path
from . import views

urlpatterns = [
    path("cookies/", views.cookies, name="cookies"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_and_conditions/", views.terms_and_conditions, name="terms_and_conditions"),
]
