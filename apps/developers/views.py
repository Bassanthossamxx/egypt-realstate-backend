from django.db import transaction
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from apps.core.choices import UserRoles
from apps.core.permissions import IsManagerOrSuperadmin, IsStaffOrHigher
from apps.users.models import User

from .models import Developer
from .serializers import DeveloperSerializer


class DeveloperListCreateView(generics.ListCreateAPIView):
	"""List (public) + create (staff+) developers.

	Search:
	- Use `?search=...` to search by `name_en` / `name_ar`.
	"""

	queryset = Developer.objects.all().order_by('-created_at', '-id')
	serializer_class = DeveloperSerializer
	filter_backends = [SearchFilter]
	search_fields = ['name_en', 'name_ar']

	def get_permissions(self):
		if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
			return [AllowAny()]
		return [IsStaffOrHigher()]


class DeveloperRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	"""Retrieve (public) + update (staff+) + delete (manager+) developer."""

	queryset = Developer.objects.all()
	serializer_class = DeveloperSerializer

	def get_permissions(self):
		if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
			return [AllowAny()]
		if self.request.method in ['PUT', 'PATCH']:
			return [IsStaffOrHigher()]
		if self.request.method == 'DELETE':
			return [IsManagerOrSuperadmin()]
		return [AllowAny()]

	@transaction.atomic
	def perform_destroy(self, instance: Developer) -> None:
		# When a developer is deleted, any related user accounts become customers.
		User.objects.filter(developer=instance).update(role=UserRoles.CUSTOMER, developer=None)

		# Backward compatibility: if a direct user link exists, demote it too.
		if instance.user_id:
			User.objects.filter(id=instance.user_id).update(role=UserRoles.CUSTOMER, developer=None)
			instance.user = None
			instance.save(update_fields=['user'])

		instance.delete()
