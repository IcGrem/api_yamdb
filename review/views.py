from rest_framework import permissions, viewsets, generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from .models import User, Review, Comment, Title, Category, Genre
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    UserSerializer
)
from .permissions import IsAuthorOrReadOnlyPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)#OrReadOnly,)


# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)#OrReadOnly,)


# class MeProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)#OrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(genres=self.genres, categories=self.categories)


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['name']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

class GenreViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['name']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class ReviewViewSet(viewsets.ModelViewSet):
    #queryset = Post.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]#, IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(title_id=self.kwargs.get('title_id'), author=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.filter(title_id=self.kwargs.get('title_id'))
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]#, IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.filter(review__title_id=self.kwargs.get('title_id'), review_id=self.kwargs.get('review_id'))
        return queryset
