from rest_framework import permissions, viewsets, generics, filters, status
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
from .filters import GenreFilter

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
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['=genres__slug']
    filter_class = GenreFilter
    # def perform_create(self, serializer):
    #     serializer.save(genres=self.genres, categories=self.categories)


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    # def get_object(self):
    #     try:
    #         # Perform the lookup filtering.
    #         lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

    #         assert lookup_url_kwarg in self.kwargs, (
    #             (self.__class__.__name__, lookup_url_kwarg)
    #         )

    #         filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    #         queryset = self.filter_queryset(self.get_queryset())
    #         obj = get_object_or_404(queryset, **filter_kwargs)
    #     except Http404:
    #         if self.request.method in ['DELETE','GET','PATCH']:
    #             raise MethodNotAllowed(self.request.method)
    #         raise Http404
    #     # May raise a permission denied
    #     self.check_object_permissions(self.request, obj)

    #     return obj

    
    # def create(self, request, *args, **kwargs):
    #     # if not request.user.is_authenticated:
    #     #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        serializer.save(author=self.request.user, title_id=self.kwargs.get('title_id'))

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
