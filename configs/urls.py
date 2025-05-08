"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from configs.views import HomePage, ErrorPage

handler400 = lambda request, exception: ErrorPage(request, exception, 400)
handler403 = lambda request, exception: ErrorPage(request, exception, 403)
handler404 = lambda request, exception: ErrorPage(request, exception, 404)
handler500 = lambda request: ErrorPage(request, None, 500)

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("", HomePage, name="homepage"),
    path('admin/', admin.site.urls),
    path("services/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("services/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("services/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
