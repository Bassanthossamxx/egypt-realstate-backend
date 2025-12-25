from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    CUSTOMER = 'customer', _('Customer')
    DEVELOPER = 'developer', _('Developer')
    CONTENT_CREATOR = 'content_creator', _('Content Creator')
    STAFF = 'staff', _('Staff')
    MANAGER = 'manager', _('Manager')
    SUPERADMIN = 'superadmin', _('Superadmin')


class UserManager(BaseUserManager):
    """Custom user manager for User model with email as the unique identifier."""
    
    def create_user(self, email, full_name, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not full_name:
            raise ValueError(_('The Full Name field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRoles.SUPERADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=255)
    phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
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
        null=True
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
