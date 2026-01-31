from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.core.permissions import IsCustomer, IsStaffOrHigher
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    CustomerInquirySerializer,
    CustomerInquiryContactSerializer,
    token_expiry_info,
)
from .models import User, CustomerInquiry


class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.
    Creates a new user with Customer role by default.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        expiry = token_expiry_info(refresh)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user, context={'request': request}).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            **expiry,
        }, status=status.HTTP_201_CREATED)


RegisterView = extend_schema_view(
    post=extend_schema(tags=['Auth'], summary='Register (public)'),
)(RegisterView)


class LoginView(TokenObtainPairView):
    """
    Login with email and password.
    Returns access and refresh tokens with user data and role.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


LoginView = extend_schema_view(
    post=extend_schema(tags=['Auth'], summary='Login (public)'),
)(LoginView)


class LogoutView(APIView):
    """
    Logout the current user by blacklisting the refresh token.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Successfully logged out'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


LogoutView = extend_schema_view(
    post=extend_schema(tags=['Auth'], summary='Logout (blacklist refresh token)'),
)(LogoutView)


class MeView(generics.RetrieveUpdateAPIView):
    """
    Get or update current user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


MeView = extend_schema_view(
    get=extend_schema(tags=['Auth'], summary='Get current user (me)'),
    patch=extend_schema(tags=['Auth'], summary='Update current user (me)'),
    put=extend_schema(tags=['Auth'], summary='Update current user (me) - full'),
)(MeView)


class CustomerInquiryListCreateView(generics.ListCreateAPIView):
    queryset = CustomerInquiry.objects.select_related('customer').all()
    serializer_class = CustomerInquirySerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [IsStaffOrHigher()]
        if self.request.method == 'POST':
            return [IsCustomer()]
        return []

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


CustomerInquiryListCreateView = extend_schema_view(
    get=extend_schema(tags=['Customer'], summary='List customer inquiries (staff+)'),
    post=extend_schema(tags=['Customer'], summary='Create inquiry (customer)'),
)(CustomerInquiryListCreateView)


class CustomerInquiryContactUpdateView(generics.UpdateAPIView):
    queryset = CustomerInquiry.objects.all()
    serializer_class = CustomerInquiryContactSerializer
    http_method_names = ['patch', 'options', 'head']

    def get_permissions(self):
        return [IsStaffOrHigher()]


CustomerInquiryContactUpdateView = extend_schema_view(
    patch=extend_schema(tags=['Customer'], summary='Mark inquiry contacted (staff+)'),
)(CustomerInquiryContactUpdateView)

