from django.shortcuts import render
from rest_framework import viewsets, status, filters
from .models import Categories, Genre, Title
from .serializers import (
    CategoriesSerializer,
    GenreSerializer,
    TitleSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import MethodNotAllowed
from django.http import Http404


class CategoriesViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    queryset = Categories.objects.all()

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """

        try:
            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
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

    
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GenreViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    queryset = Genre.objects.all()

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """

        try:
            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                    'Expected view %s to be called with a URL keyword argument '
                    'named "%s". Fix your URL conf, or set the `.lookup_field` '
                    'attribute on the view correctly.' %
                    (self.__class__.__name__, lookup_url_kwarg)
            )

            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, **filter_kwargs)
        except Http404:
            if self.request.method in ['DELETE', 'GET', 'PATCH']:
                raise MethodNotAllowed(self.request.method)
            raise Http404
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['category', 'genre', 'name', 'year']
    queryset = Title.objects.all()





