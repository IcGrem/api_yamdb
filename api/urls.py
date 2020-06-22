from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import CategoriesViewSet, GenreViewSet, TitleViewSet
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_nested import routers


router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
