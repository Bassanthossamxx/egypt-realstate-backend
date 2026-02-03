from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Q

from apps.core.permissions import IsManagerOrSuperadmin
from apps.core.choices import UserRoles

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

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Superusers can see all users
        if user.is_superuser or user.role == UserRoles.SUPERUSER:
            return queryset
        
        # Managers can only see users with roles from manager and below (exclude superusers)
        if user.role == UserRoles.MANAGER:
            return queryset.exclude(
                Q(role=UserRoles.SUPERUSER) | Q(is_superuser=True)
            )
        
        return queryset

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
