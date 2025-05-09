from django.urls import path, include
from rest_framework.routers import DefaultRouter
from googleApp.views import FinancialDataViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'financial-data', FinancialDataViewSet, basename='financial-data')

googleApp_urlpatterns = [
    path('', include(router.urls)),
]
