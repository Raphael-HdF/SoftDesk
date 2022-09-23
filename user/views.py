from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.serializers import RegisterUserSerializer, UserListSerializer


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
            return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
