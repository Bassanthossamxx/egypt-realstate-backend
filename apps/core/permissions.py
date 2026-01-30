"""
Role-based permission classes for the Real Estate Backend.
All authorization rules are enforced at the view level.

Usage Example:
    # For public GET requests - anyone can view
    permission_classes = [AllowAny]  # or IsAnonymousUser
    
    # For articles - only content creators, managers, and superusers
    permission_classes = [IsContentCreator | IsManager | IsSuperuser]
    
    # For staff operations
    permission_classes = [IsStaffOrHigher]
"""
from rest_framework import permissions
from apps.core.choices import UserRoles


# ============================================================================
# Base Role Permission Classes
# ============================================================================

class IsAnonymousUser(permissions.BasePermission):
    """
    Permission for anonymous (unauthenticated) users.
    Can only view public content (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return not request.user.is_authenticated
        return False


class IsCustomer(permissions.BasePermission):
    """
    Permission for Customer role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == UserRoles.CUSTOMER
        )


class IsDeveloper(permissions.BasePermission):
    """
    Permission for Developer role.
    Automatically checks if user is active.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == UserRoles.DEVELOPER and
            request.user.is_active
        )


class IsContentCreator(permissions.BasePermission):
    """
    Permission for Content Creator role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == UserRoles.CONTENT_CREATOR
        )


class IsStaff(permissions.BasePermission):
    """
    Permission for Staff role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == UserRoles.STAFF
        )


class IsManager(permissions.BasePermission):
    """
    Permission for Manager role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == UserRoles.MANAGER
        )


class IsSuperuser(permissions.BasePermission):
    """
    Permission for Superuser role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == UserRoles.SUPERUSER
        )


# Backward-compatible alias
IsSuperadmin = IsSuperuser


# ============================================================================
# Combined Role Permission Classes (Helpers)
# ============================================================================

class IsStaffOrHigher(permissions.BasePermission):
    """
    Permission for Staff, Manager, or Superuser roles.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [
                UserRoles.STAFF,
                UserRoles.MANAGER,
                UserRoles.SUPERUSER
            ]
        )


class IsManagerOrSuperadmin(permissions.BasePermission):
    """
    Permission for Manager or Superuser roles.
    Useful for delete operations and role upgrades.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [UserRoles.MANAGER, UserRoles.SUPERUSER]
        )


class IsAuthenticated(permissions.BasePermission):
    """
    Permission for any authenticated user.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
