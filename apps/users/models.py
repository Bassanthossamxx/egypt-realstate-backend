from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from apps.core.choices import UserRoles
from apps.core.validation import (
    validate_phone_number,
)


class UserManager(BaseUserManager):
    """Custom user manager that uses email instead of username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRoles.SUPERADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password=password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=255)
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        null=True,
        validators=[validate_phone_number],
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.CUSTOMER
    )
    profile_image = models.ImageField(
        _('profile image'),
        upload_to='users/profiles/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def is_superadmin(self):
        return self.role == UserRoles.SUPERADMIN

    @property
    def is_manager(self):
        return self.role == UserRoles.MANAGER

    @property
    def is_staff_member(self):
        return self.role == UserRoles.STAFF

    @property
    def is_developer(self):
        return self.role == UserRoles.DEVELOPER

    @property
    def is_content_creator(self):
        return self.role == UserRoles.CONTENT_CREATOR

    @property
    def is_customer(self):
        return self.role == UserRoles.CUSTOMER


class CustomerInquiry(models.Model):
    customer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='customer_inquiries'
    )
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        validators=[validate_phone_number],
    ) 
    message = models.TextField(_('message'))
    #todo : change to choices of unit types later
    interested_in = models.CharField(_('interested in'), max_length=100)

    # Project/Unit models are not present in the codebase yet.
    # Store their IDs as optional integers to match the ERD intent.
    project_id = models.PositiveBigIntegerField(_('project id'), blank=True, null=True)
    unit_id = models.PositiveBigIntegerField(_('unit id'), blank=True, null=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('customer inquiry')
        verbose_name_plural = _('customer inquiries')
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry #{self.id} by {self.customer_id}"
