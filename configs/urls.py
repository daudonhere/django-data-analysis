from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from configs.views import HomePage, ErrorPage, IngestionDataViewSet
from financeApp.urls import financeApp_urlpatterns
from economyApp.urls import economyApp_urlpatterns
from trendApp.urls import trendApp_urlpatterns

handler400 = lambda request, exception: ErrorPage(request, exception, 400)
handler403 = lambda request, exception: ErrorPage(request, exception, 403)
handler404 = lambda request, exception: ErrorPage(request, exception, 404)
handler500 = lambda request: ErrorPage(request, None, 500)

router = DefaultRouter(trailing_slash=False)

router.register(r'ingestion', IngestionDataViewSet, basename='ingestion')
ingestionUrl_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path("", HomePage, name="homepage"),
    path('admin/', admin.site.urls),
    path("services/v1/", include((ingestionUrl_urlpatterns, "ingestionUrl"), namespace="ingestionUrl")),
    path("services/v1/", include((economyApp_urlpatterns, "economyApp"), namespace="economyApp")),
    path("services/v1/", include((financeApp_urlpatterns, "financeApp"), namespace="financeApp")),
    path("services/v1/", include((trendApp_urlpatterns, "trendApp"), namespace="trendApp")),
    path("services/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("services/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("services/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
