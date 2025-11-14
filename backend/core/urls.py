from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse

def health(_):  # simple function-based view
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("admin/", admin.site.urls),

    # Apps
    path("api/projects/", include("projects.urls")),
    path("api/assistant/", include("assistant.urls")),

    # Auth (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API schema & docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    # Health-ping
    path("api/health/", health, name="health"),
]
