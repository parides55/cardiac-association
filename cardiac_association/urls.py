"""
URL configuration for cardiac_association project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path("", include("home_page.urls"), name="home_page"),
    path("about_us/", include("about_us.urls"), name="about_us"),
    path("events/", include("events.urls"), name="events"),
    path("news/", include("news.urls"), name="news"),
    path("what_we_do/", include("what_we_do.urls"), name="what_we_do"),
    path("how_you_can_help/", include("how_you_can_help.urls"), name="how_you_can_help"),
    path("shop/", include("shop.urls"), name="shop"),
)
