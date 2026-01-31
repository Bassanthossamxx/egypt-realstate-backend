"""
ViewSets for core models with role-based permissions.
"""
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Country, City, Slider, Ad, Feature, Article
from .serializers import (
    CountrySerializer,
    CitySerializer,
    SliderSerializer,
    AdSerializer,
    FeatureSerializer,
    ArticleSerializer
)
from .permissions import (
    IsStaff,
    IsManager,
    IsSuperuser,
    IsContentCreator,
    IsManagerOrSuperadmin
)


def _parse_bool_query(value: str | None) -> bool | None:
    if value is None:
        return None

    value = value.strip().lower()
    if value in {"true", "1", "yes", "y", "t"}:
        return True
    if value in {"false", "0", "no", "n", "f"}:
        return False
    return None



class CountryViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Countries.
    
    Permissions:
    - Anyone can view (GET)
    - Staff can create and edit (POST, PUT, PATCH)
    - Manager and Superuser can delete (DELETE)
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name_en", "name_ar"]

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, "action", None) == "list":
            raw = self.request.query_params.get("appear_on_home_page")
            if raw is None:
                return qs.filter(appear_on_home_page=True)
            if raw.strip().lower() == "all":
                return qs
            parsed = _parse_bool_query(raw)
            if parsed is None:
                return qs.filter(appear_on_home_page=True)
            return qs.filter(appear_on_home_page=parsed)
        return qs
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]


CountryViewSet = extend_schema_view(
    list=extend_schema(tags=['Core'], summary='List countries (public)'),
    retrieve=extend_schema(tags=['Core'], summary='Retrieve country (public)'),
    create=extend_schema(tags=['Core'], summary='Create country (staff+)'),
    update=extend_schema(tags=['Core'], summary='Update country (staff+)'),
    partial_update=extend_schema(tags=['Core'], summary='Partially update country (staff+)'),
    destroy=extend_schema(tags=['Core'], summary='Delete country (manager+)'),
)(CountryViewSet)



class CityViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Cities.
    
    Permissions:
    - Anyone can view (GET)
    - Staff can create and edit (POST, PUT, PATCH)
    - Manager and Superuser can delete (DELETE)
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name_en", "name_ar"]

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, "action", None) == "list":
            raw = self.request.query_params.get("appear_on_home_page")
            if raw is None:
                return qs.filter(appear_on_home_page=True)
            if raw.strip().lower() == "all":
                return qs
            parsed = _parse_bool_query(raw)
            if parsed is None:
                return qs.filter(appear_on_home_page=True)
            return qs.filter(appear_on_home_page=parsed)
        return qs
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]


CityViewSet = extend_schema_view(
    list=extend_schema(tags=['Core'], summary='List cities (public)'),
    retrieve=extend_schema(tags=['Core'], summary='Retrieve city (public)'),
    create=extend_schema(tags=['Core'], summary='Create city (staff+)'),
    update=extend_schema(tags=['Core'], summary='Update city (staff+)'),
    partial_update=extend_schema(tags=['Core'], summary='Partially update city (staff+)'),
    destroy=extend_schema(tags=['Core'], summary='Delete city (manager+)'),
)(CityViewSet)



class SliderViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Sliders (home page images).
    
    Permissions:
    - Anyone can view (GET)
    - Staff can create and edit (POST, PUT, PATCH)
    - Manager and Superuser can delete (DELETE)
    """
    queryset = Slider.objects.all().order_by('index', 'id')
    serializer_class = SliderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, "action", None) == "list":
            raw = self.request.query_params.get("appear_on_home_page")
            if raw is None:
                return qs.filter(appear_on_home_page=True)
            if raw.strip().lower() == "all":
                return qs
            parsed = _parse_bool_query(raw)
            if parsed is None:
                return qs.filter(appear_on_home_page=True)
            return qs.filter(appear_on_home_page=parsed)
        return qs
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]


SliderViewSet = extend_schema_view(
    list=extend_schema(tags=['Core'], summary='List sliders (public)'),
    retrieve=extend_schema(tags=['Core'], summary='Retrieve slider (public)'),
    create=extend_schema(tags=['Core'], summary='Create slider (staff+)'),
    update=extend_schema(tags=['Core'], summary='Update slider (staff+)'),
    partial_update=extend_schema(tags=['Core'], summary='Partially update slider (staff+)'),
    destroy=extend_schema(tags=['Core'], summary='Delete slider (manager+)'),
)(SliderViewSet)



class AdViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Advertisements.
    
    Permissions:
    - Anyone can view (GET)
    - Staff can create and edit (POST, PUT, PATCH)
    - Manager and Superuser can delete (DELETE)
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]


AdViewSet = extend_schema_view(
    list=extend_schema(tags=['Core'], summary='List ads (public)'),
    retrieve=extend_schema(tags=['Core'], summary='Retrieve ad (public)'),
    create=extend_schema(tags=['Core'], summary='Create ad (staff+)'),
    update=extend_schema(tags=['Core'], summary='Update ad (staff+)'),
    partial_update=extend_schema(tags=['Core'], summary='Partially update ad (staff+)'),
    destroy=extend_schema(tags=['Core'], summary='Delete ad (manager+)'),
)(AdViewSet)


class FeatureViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Features (property features).
    
    Permissions:
    - Anyone can view (GET)
    - Staff can create and edit (POST, PUT, PATCH)
    - Manager and Superuser can delete (DELETE)
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name_en", "name_ar"]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]


FeatureViewSet = extend_schema_view(
    list=extend_schema(tags=['Core'], summary='List features (public)'),
    retrieve=extend_schema(tags=['Core'], summary='Retrieve feature (public)'),
    create=extend_schema(tags=['Core'], summary='Create feature (staff+)'),
    update=extend_schema(tags=['Core'], summary='Update feature (staff+)'),
    partial_update=extend_schema(tags=['Core'], summary='Partially update feature (staff+)'),
    destroy=extend_schema(tags=['Core'], summary='Delete feature (manager+)'),
)(FeatureViewSet)



class ArticleViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Articles.
    
    Permissions:
    - Anyone can view (GET)
    - Content Creator, Manager, or Superuser can create, edit, and delete (POST, PUT, PATCH, DELETE)
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title_en", "title_ar"]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsContentCreator | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [(IsContentCreator | IsManager | IsSuperuser)()]
        return [AllowAny()]


ArticleViewSet = extend_schema_view(
    list=extend_schema(tags=['Core'], summary='List articles (public)'),
    retrieve=extend_schema(tags=['Core'], summary='Retrieve article (public)'),
    create=extend_schema(tags=['Core'], summary='Create article (content_creator/manager/superuser)'),
    update=extend_schema(tags=['Core'], summary='Update article (content_creator/manager/superuser)'),
    partial_update=extend_schema(tags=['Core'], summary='Partially update article (content_creator/manager/superuser)'),
    destroy=extend_schema(tags=['Core'], summary='Delete article (content_creator/manager/superuser)'),
)(ArticleViewSet)
