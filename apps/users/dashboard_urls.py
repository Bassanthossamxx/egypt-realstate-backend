from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .dashboard_views import DashboardUserViewSet

router = DefaultRouter()
router.register(r'users', DashboardUserViewSet, basename='dashboard-users')

urlpatterns = [
    path('', include(router.urls)),
]
