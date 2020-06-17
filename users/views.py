from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from .pagination import CustomPagination
from users.models import User
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from users.serializers import UserRegistrationSerializer, MyAuthTokenSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

class ObtainAuthToken(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyAuthTokenSerializer
    queryset = User.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
        ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
