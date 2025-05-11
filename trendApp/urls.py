from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trendApp.views import SearchTrendViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'finance', SearchTrendViewSet, basename='finance')

trendApp_urlpatterns = [
    path('', include(router.urls)),
]
