from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

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


DashboardUserViewSet = extend_schema_view(
    list=extend_schema(tags=['Dashboard Users'], summary='List users (manager/superuser)'),
    retrieve=extend_schema(tags=['Dashboard Users'], summary='Retrieve user (manager/superuser)'),
    create=extend_schema(tags=['Dashboard Users'], summary='Create user (manager/superuser)'),
    update=extend_schema(tags=['Dashboard Users'], summary='Update user (manager/superuser)'),
    partial_update=extend_schema(tags=['Dashboard Users'], summary='Partially update user (manager/superuser)'),
    destroy=extend_schema(tags=['Dashboard Users'], summary='Delete user (manager/superuser)'),
)(DashboardUserViewSet)
