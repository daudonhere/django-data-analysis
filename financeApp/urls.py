from django.urls import path, include
from rest_framework.routers import DefaultRouter
from financeApp.views import FinancialDataViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'finances', FinancialDataViewSet, basename='finances')

financeApp_urlpatterns = [
    path('', include(router.urls)),
]
