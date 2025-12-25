"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CountryViewSet,
    CityViewSet,
    SliderViewSet,
    AdViewSet,
    FeatureViewSet,
    ArticleViewSet
)

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'sliders', SliderViewSet, basename='slider')
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'features', FeatureViewSet, basename='feature')
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
]
