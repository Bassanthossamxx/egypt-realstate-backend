from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.permissions import IsStaff, IsManager, IsSuperuser, IsManagerOrSuperadmin
from .models import UnitType
from .serializers import UnitTypeSerializer


class UnitTypeViewSet(viewsets.ModelViewSet):
	queryset = UnitType.objects.all().order_by('id')
	serializer_class = UnitTypeSerializer
	filter_backends = [SearchFilter]
	search_fields = ['name_en', 'name_ar']

	def get_permissions(self):
		if self.action in ['list', 'retrieve']:
			return [AllowAny()]
		if self.action in ['create', 'update', 'partial_update']:
			return [(IsStaff | IsManager | IsSuperuser)()]
		if self.action == 'destroy':
			return [IsManagerOrSuperadmin()]
		return [AllowAny()]


UnitTypeViewSet = extend_schema_view(
	list=extend_schema(tags=['Units'], summary='List unit types (public)'),
	retrieve=extend_schema(tags=['Units'], summary='Retrieve unit type (public)'),
	create=extend_schema(tags=['Units'], summary='Create unit type (staff+)'),
	update=extend_schema(tags=['Units'], summary='Update unit type (staff+)'),
	partial_update=extend_schema(tags=['Units'], summary='Partially update unit type (staff+)'),
	destroy=extend_schema(tags=['Units'], summary='Delete unit type (manager+)'),
)(UnitTypeViewSet)
