from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.core.permissions import IsStaff, IsManager, IsSuperuser, IsManagerOrSuperadmin
from .models import UnitType
from .serializers import UnitTypeSerializer


class UnitTypeViewSet(viewsets.ModelViewSet):
	queryset = UnitType.objects.all().order_by('id')
	serializer_class = UnitTypeSerializer

	def get_permissions(self):
		if self.action in ['list', 'retrieve']:
			return [AllowAny()]
		if self.action in ['create', 'update', 'partial_update']:
			return [(IsStaff | IsManager | IsSuperuser)()]
		if self.action == 'destroy':
			return [IsManagerOrSuperadmin()]
		return [AllowAny()]
