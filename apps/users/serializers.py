from datetime import datetime

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, CustomerInquiry
from apps.units.models import UnitType


def token_expiry_info(refresh: RefreshToken) -> dict:
    """Return expiry timestamps + remaining seconds for refresh & access tokens."""
    now = timezone.now()

    refresh_exp = int(refresh["exp"])
    refresh_expires_at = datetime.fromtimestamp(refresh_exp, tz=timezone.utc)

    access = refresh.access_token
    access_exp = int(access["exp"])
    access_expires_at = datetime.fromtimestamp(access_exp, tz=timezone.utc)

    return {
        "access_expires_at": access_expires_at.isoformat(),
        "refresh_expires_at": refresh_expires_at.isoformat(),
        "access_expires_in": max(0, int((access_expires_at - now).total_seconds())),
        "refresh_expires_in": max(0, int((refresh_expires_at - now).total_seconds())),
    }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'role',
            'profile_image',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'phone',
            'password',
            'password_confirm',
            'profile_image'
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })

        # Validate password strength
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        # Create user with Customer role by default
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        token['full_name'] = user.full_name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        expiry = token_expiry_info(refresh)
        data.update(expiry)

        # Add user data to response
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
            'role': self.user.role,
            'phone': self.user.phone,
            'profile_image': self.user.profile_image.url if self.user.profile_image else None,
        }

        return data


class CustomerInquirySerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)
    interested_in_name_en = serializers.CharField(source='interested_in.name_en', read_only=True)
    interested_in_name_ar = serializers.CharField(source='interested_in.name_ar', read_only=True)
    interested_in = serializers.PrimaryKeyRelatedField(
        queryset=UnitType.objects.all(),
        required=True,
    )

    class Meta:
        model = CustomerInquiry
        fields = [
            'id',
            'customer_id',
            'phone',
            'message',
            'interested_in',
            'interested_in_name_en',
            'interested_in_name_ar',
            'project_id',
            'unit_id',
            'is_contacted',
            'created_at',
        ]
        read_only_fields = ['id', 'customer_id', 'created_at', 'is_contacted']

    def validate(self, attrs):
        if not attrs.get('interested_in'):
            raise serializers.ValidationError({'interested_in': 'This field is required.'})

        project_id = attrs.get('project_id')
        unit_id = attrs.get('unit_id')
        if not project_id and not unit_id:
            raise serializers.ValidationError(
                'Provide project_id and/or unit_id.'
            )
        return attrs

    def create(self, validated_data):
        customer = validated_data.pop('customer', None)
        if customer is None:
            request = self.context.get('request')
            if request is None or request.user is None or not request.user.is_authenticated:
                raise serializers.ValidationError({'customer': 'Authenticated user is required.'})
            customer = request.user

        return CustomerInquiry.objects.create(customer=customer, **validated_data)


class CustomerInquiryContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInquiry
        fields = ['is_contacted']
