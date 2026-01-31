from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.core.permissions import IsManagerOrSuperadmin

from .models import User
from .serializers import AdminUserCreateSerializer, AdminUserSerializer, AdminUserUpdateSerializer


class DashboardUserViewSet(viewsets.ModelViewSet):
    """Dashboard users CRUD.

    Permissions:
    - Manager/Superuser only for all actions.
    """

    queryset = User.objects.all().select_related('developer').order_by('-created_at', '-id')

    def get_permissions(self):
        # Keep explicit: no public dashboard endpoints.
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsManagerOrSuperadmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminUserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return AdminUserUpdateSerializer
        return AdminUserSerializer
