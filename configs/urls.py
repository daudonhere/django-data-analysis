from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from configs.views import HomePage, ErrorPage
from financeApp.urls import financeApp_urlpatterns
from economyApp.urls import economyApp_urlpatterns

handler400 = lambda request, exception: ErrorPage(request, exception, 400)
handler403 = lambda request, exception: ErrorPage(request, exception, 403)
handler404 = lambda request, exception: ErrorPage(request, exception, 404)
handler500 = lambda request: ErrorPage(request, None, 500)

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("", HomePage, name="homepage"),
    path('admin/', admin.site.urls),
    path("services/", include((economyApp_urlpatterns, "economyApp"), namespace="economyApp")),
    path("services/", include((financeApp_urlpatterns, "financeApp"), namespace="financeApp")),
    path("services/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("services/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("services/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
