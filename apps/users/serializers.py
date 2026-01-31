from datetime import datetime

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, CustomerInquiry
from apps.units.models import UnitType
from apps.core.choices import UserRoles
from apps.developers.models import Developer


def token_expiry_info(refresh: RefreshToken) -> dict:
    """Return expiry timestamps + remaining seconds for refresh & access tokens."""
    now = timezone.now()

    refresh_exp = int(refresh["exp"])
    refresh_expires_at = datetime.fromtimestamp(refresh_exp, tz=timezone.UTC)

    access = refresh.access_token
    access_exp = int(access["exp"])
    access_expires_at = datetime.fromtimestamp(access_exp, tz=timezone.UTC)

    return {
        "access_expires_at": access_expires_at.isoformat(),
        "refresh_expires_at": refresh_expires_at.isoformat(),
        "access_expires_in": max(0, int((access_expires_at - now).total_seconds())),
        "refresh_expires_in": max(0, int((refresh_expires_at - now).total_seconds())),
    }


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = getattr(self, "context", {}).get("request")
        if request and isinstance(data.get("profile_image"), str) and data["profile_image"].startswith("/"):
            data["profile_image"] = request.build_absolute_uri(data["profile_image"])
        return data

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
        request = self.context.get('request')

        profile_image_url = None
        if self.user.profile_image:
            raw_url = self.user.profile_image.url
            profile_image_url = request.build_absolute_uri(raw_url) if request else raw_url

        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
            'role': self.user.role,
            'phone': self.user.phone,
            'profile_image': profile_image_url,
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


class AdminUserSerializer(serializers.ModelSerializer):
    developer_id = serializers.IntegerField(source='developer.id', read_only=True)
    developer_name_en = serializers.CharField(source='developer.name_en', read_only=True)
    developer_name_ar = serializers.CharField(source='developer.name_ar', read_only=True)
    developer_logo = serializers.ImageField(source='developer.logo', read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = getattr(self, 'context', {}).get('request')
        if request:
            if isinstance(data.get('profile_image'), str) and data['profile_image'].startswith('/'):
                data['profile_image'] = request.build_absolute_uri(data['profile_image'])
            if isinstance(data.get('developer_logo'), str) and data['developer_logo'].startswith('/'):
                data['developer_logo'] = request.build_absolute_uri(data['developer_logo'])
        return data

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'role',
            'developer_id',
            'developer_name_en',
            'developer_name_ar',
            'developer_logo',
            'profile_image',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    developer_id = serializers.PrimaryKeyRelatedField(
        source='developer',
        queryset=Developer.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'role',
            'developer_id',
            'profile_image',
            'is_active',
            'password',
            'password_confirm',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({'password': "Password fields didn't match."})

        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        role = attrs.get('role')
        developer = attrs.get('developer')
        if role == UserRoles.DEVELOPER and developer is None:
            raise serializers.ValidationError({'developer_id': 'Developer is required when role is developer.'})
        if role != UserRoles.DEVELOPER:
            attrs['developer'] = None

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    developer_id = serializers.PrimaryKeyRelatedField(
        source='developer',
        queryset=Developer.objects.all(),
        required=False,
        allow_null=True,
    )
    new_password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'full_name',
            'phone',
            'role',
            'developer_id',
            'profile_image',
            'is_active',
            'new_password',
            'new_password_confirm',
        ]

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

        if (new_password and not new_password_confirm) or (new_password_confirm and not new_password):
            raise serializers.ValidationError({'new_password': 'Provide new_password and new_password_confirm.'})

        if new_password:
            if new_password != new_password_confirm:
                raise serializers.ValidationError({'new_password': "Password fields didn't match."})
            try:
                validate_password(new_password)
            except ValidationError as e:
                raise serializers.ValidationError({'new_password': list(e.messages)})

        # Role/developer relationship enforcement
        role = attrs.get('role', getattr(self.instance, 'role', None))
        developer = attrs.get('developer', getattr(self.instance, 'developer', None))

        if role == UserRoles.DEVELOPER and developer is None:
            raise serializers.ValidationError({'developer_id': 'Developer is required when role is developer.'})

        if role != UserRoles.DEVELOPER:
            attrs['developer'] = None

        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('new_password_confirm', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance
