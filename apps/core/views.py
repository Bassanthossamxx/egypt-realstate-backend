"""
ViewSets for core models with role-based permissions.
"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

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
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]



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
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]



class SliderViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Sliders (home page images).
    
    Permissions:
    - Anyone can view (GET)
    - Staff can create and edit (POST, PUT, PATCH)
    - Manager and Superuser can delete (DELETE)
    """
    queryset = Slider.objects.all().order_by('index')
    serializer_class = SliderSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]



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
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsStaff | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]



class ArticleViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Articles.
    
    Permissions:
    - Anyone can view (GET)
    - Content Creator, Manager, or Superuser can create, edit, and delete (POST, PUT, PATCH, DELETE)
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [(IsContentCreator | IsManager | IsSuperuser)()]
        elif self.action == 'destroy':
            return [(IsContentCreator | IsManager | IsSuperuser)()]
        return [AllowAny()]
