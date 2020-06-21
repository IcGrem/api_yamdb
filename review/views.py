from rest_framework import permissions, viewsets, generics, filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
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
    UserRegistrationSerializer,
    MyAuthTokenSerializer,
    UserSerializer
)
from .permissions import (
    IsAdminPermission,
    IsModeratorPermission,
    IsOwnerPermission,
)
from .filters import GenreFilter
from rest_framework.exceptions import MethodNotAllowed
from django.http import Http404


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

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = GenreFilter
    pagination_class = PageNumberPagination

    # def perform_create(self, serializer):
    #     serializer.save(genres=self.genres, categories=self.categories)

    # def list(self, *args, **kwargs):
    #     permission_classes = [permissions.AllowAny]
    #     serializer = TitleSerializer(self.queryset, many=True)
    #     return Response(serializer.data)
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAuthorOrReadOnly|permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def get_object(self):
        try:
            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                (self.__class__.__name__, lookup_url_kwarg)
            )

            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, **filter_kwargs)
        except Http404:
            if self.request.method in ['DELETE','GET','PATCH']:
                raise MethodNotAllowed(self.request.method)
            raise Http404
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    
    # def create(self, request, *args, **kwargs):
    #     # if not request.user.is_authenticated:
    #     #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]


class GenreViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (permissions.IsAuthenticated,)
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['name']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    # def perform_create(self, serializer):
    #     #title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
    #     genre = Genre.objects.filter(slug=self.kwargs.get('slug')
    #     if self.request.method == 'GET' and genre.count() == 0:
    #         raise MethodNotAllowed(self.request.method)
    #     serializer.save(slug=genre.slug)
    def get_object(self):
        try:
            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                (self.__class__.__name__, lookup_url_kwarg)
            )

            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, **filter_kwargs)
        except Http404:
            if self.request.method in ['DELETE','GET','PATCH']:
                raise MethodNotAllowed(self.request.method)
            raise Http404
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]


class ReviewViewSet(viewsets.ModelViewSet):
    #lookup_field = 'reviews'
    serializer_class = ReviewSerializer
    #permission_classes = [permissions.AllowAny|permissions.IsAuthenticated]#, IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = Review.objects.filter(title_id=title.id, author=self.request.user)
        if self.request.method == 'POST' and review:
            raise ValidationError('Можно оставить только один отзыв на одно произведение.')
        if self.request.method == 'PATCH' and review.author!=self.request.user and self.request.user.role=='user':
            raise ValidationError('Попытка изменить чужой отзыв.')
        serializer.save(author=self.request.user, title_id=title.id)

    def get_queryset(self):
        queryset = Review.objects.filter(title_id=self.kwargs.get('title_id'))
        return queryset
    
    # @permission_classes([permissions.AllowAny])
    # def list(self, request, title_id):
    #     #reviews = Comment.objects.filter(post=post_pk)
    #     serializer = ReviewSerializer(queryset, many=True)
    #     return Response(serializer.data)
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        # elif self.action == 'destroy':#or self.action == 'partial_update'
        #     permission_classes = [permissions.IsAuthenticated&(IsOwnerPermission|IsAdminPermission|IsModeratorPermission)]
        else:
            permission_classes = [IsOwnerPermission|IsAdminPermission|IsModeratorPermission]
        return [permission() for permission in permission_classes]

    # def create(self, request, title_id):
    #     review = Review.objects.filter(title_id=title_id, author=self.request.user)
    #     if self.request.method == 'POST' and review:
    #         raise ValidationError('Можно оставить только один отзыв на одно произведение.')
    #     serializer = ReviewSerializer(data=request.data)
    #     if serializer.is_valid():
    #         #serializer.post = post_id
    #         serializer.save(author=self.request.user, title_id=title_id)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def partial_update(self, request, title_id, pk=None):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if review.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save(author=request.user, title_id=title_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, title_id, pk=None):
    #     review = get_object_or_404(Review, pk=pk)
    #     if review.author != request.user:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     review.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    #lookup_field = 'comments'
    serializer_class = CommentSerializer
    #permission_classes = [permissions.IsAuthenticated]#, IsAuthorOrReadOnlyPermission]
    #permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        #comment = Comment.objects.filter(review_id=review.id, author=self.request.user)
        #if self.request.method == 'PATCH' and comment.author!=self.request.user and self.request.user.role=='user':
            #raise ValidationError('Попытка изменить чужой отзыв.')
        serializer.save(author=self.request.user, review_id=self.kwargs.get('review_id'))

    def get_queryset(self):
        queryset = Comment.objects.filter(review__title_id=self.kwargs.get('title_id'), review_id=self.kwargs.get('review_id'))
        return queryset

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated&(IsOwnerPermission|IsAdminPermission|IsModeratorPermission)]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated&(IsOwnerPermission|IsAdminPermission|IsModeratorPermission)]
        else:
            permission_classes = [IsOwnerPermission|IsAdminPermission|IsModeratorPermission]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, title_id, review_id, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save(author=request.user, review_id=review_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, title_id, review_id, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author != request.user and request.user.role != 'moderator':# and request.user.role not in ('user','moderator','admin'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
