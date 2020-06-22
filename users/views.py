from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsAdminPermission, IsModeratorPermission
from users.models import User
from users.serializers import (
    UserRegistrationSerializer,
    MyAuthTokenSerializer,
    UserSerializer
    )
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
    permission_classes = [IsAdminPermission, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, username=None):
        try:
            usename = self.kwargs['username']
        except Exception:
            queryset = User.objects.all()
            return queryset
        if usename == 'me':
            queryset = User.objects.filter(email=self.request.user.email)
            return queryset
        queryset = User.objects.filter(username=usename)
        return queryset

    def destroy(self, request, username=None):
        if username is None or username == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
