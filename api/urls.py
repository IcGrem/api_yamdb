from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import CategoriesViewSet, GenreViewSet, TitleViewSet
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

#commets_router = routers.NestedSimpleRouter(router, r'categories', lookup='slug')
#commets_router.register(r'comments', CategoriesViewSet, basename='categories')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    #path('', include(commets_router.urls))
]

