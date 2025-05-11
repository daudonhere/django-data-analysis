from django.urls import path, include
from rest_framework.routers import DefaultRouter
from googleApp.views import GoogleTrendViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'google', GoogleTrendViewSet, basename='google')

googleApp_urlpatterns = [
    path('', include(router.urls)),
]
