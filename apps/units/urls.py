from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UnitTypeViewSet

router = DefaultRouter()
router.register(r'unit/types', UnitTypeViewSet, basename='unit-type')

urlpatterns = [
    path('', include(router.urls)),
]
