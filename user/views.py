from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, BasePermission, \
    SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.serializers import RegisterUserSerializer, UserListSerializer, \
    UserDetailsSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    detail_serializer_class = UserDetailsSerializer

    def post(self, request, *args, **kwargs):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            reg_serializer = UserDetailsSerializer(new_user)
            if new_user:
                return Response(reg_serializer.data, status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailsSerializer
    permission_classes = [IsAdminUser | ReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_active=True)
