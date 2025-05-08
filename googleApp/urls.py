from django.urls import path, include
from rest_framework.routers import DefaultRouter
from googleApp.views import GoogleTrendsViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'google-trends', GoogleTrendsViewSet, basename='google-trends')

googleApp_urlpatterns = [
    path('', include(router.urls)),
]
