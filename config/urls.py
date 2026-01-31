from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from apps.core.media_views import db_media_serve


def _superuser_only_admin_has_permission(request):
    return request.user.is_active and request.user.is_superuser


admin.site.has_permission = _superuser_only_admin_has_permission

urlpatterns = [
    # DB-backed media files
    path("media/<path:path>", db_media_serve, name="db-media"),
    path("admin/", admin.site.urls),
    # Authentication
    path("api/auth/", include("apps.users.urls")),
    # Customer
    path("api/customer/", include("apps.users.customer_urls")),
    # Core API
    path("api/", include("apps.core.urls")),
    # Units API
    path("api/", include("apps.units.urls")),
    # Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
