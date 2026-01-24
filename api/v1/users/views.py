from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from api.core.pagination import CustomPagination
from api.v1.users.models import CustomUser
from api.v1.users.permissions import IsOwner
from api.v1.users.serializers import UserSerializer, RegisterUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User class with CRUD methods

    Provide next methods:
        — list
        — create
        — destroy
        — retrieve
        — update
        — partial_update
        — login
    """
    serializer_class = UserSerializer
    queryset = CustomUser.objects.prefetch_related('notes')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'id']
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsOwner()]
        elif self.action in ['create', 'list', 'retrieve', 'login']:
            return [AllowAny()]
        else:
            return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Register a new user,
        and returns response with JWT refresh and access tokens in cookies
        """
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        headers = self.get_success_headers(serializer.data)
        response = Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

        response.set_cookie(
            'access_token',
            str(refresh.access_token),
            domain='127.0.0.1',
            path='/',
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        response.set_cookie(
            'refresh_token',
            str(refresh),
            domain='127.0.0.1',
            path='/',
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        return response

    @action(detail=False, methods=["post"], url_path='login')
    def login(self, request):
        """
        Authenticates a user with a given username and password,
        and returns response with JWT refresh and access tokens in cookies
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = get_object_or_404(CustomUser, username=username)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        response = Response({'success': True}, status=HTTP_200_OK)
        response.set_cookie(
            'access_token',
            str(refresh.access_token),
            domain='127.0.0.1',
            path='/',
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        response.set_cookie(
            'refresh_token',
            str(refresh),
            domain='127.0.0.1',
            path='/',
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        return response

