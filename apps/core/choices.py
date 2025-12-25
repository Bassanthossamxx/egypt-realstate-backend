from django.db import models
from django.utils.translation import gettext_lazy as _


class AdAppearPlace(models.TextChoices):
    HOME = "home", "Home Page"
    PROJECTS = "projects", "Projects"
    UNITS = "units", "Units"
    OTHER = "other", "Other"

AD_APPEAR_PLACES = AdAppearPlace.choices

class UserRoles(models.TextChoices):
    CUSTOMER = 'customer', _('Customer')
    DEVELOPER = 'developer', _('Developer')
    CONTENT_CREATOR = 'content_creator', _('Content Creator')
    STAFF = 'staff', _('Staff')
    MANAGER = 'manager', _('Manager')
    SUPERADMIN = 'superadmin', _('Superadmin')
