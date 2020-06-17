from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import RegisterView, ObtainAuthToken, UserViewSet
from django.views.decorators.csrf import csrf_exempt

# router = routers.DefaultRouter()
# router.register('users', UserViewSet,  basename='users')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('auth/email/', RegisterView.as_view()),
#     path('auth/token/', ObtainAuthToken.as_view())
# ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,

# from .views import (
#     ReviewViewSet,
#     CommentViewSet,
#     TitleViewSet,
#     GenreViewSet,
#     CategoryViewSet,
#     #UserViewSet,
#     UserProfileViewSet,
#     MeProfileViewSet
# )
router = DefaultRouter()
router.register('users', UserViewSet)
router.register('users/<username>', UserViewSet)
router.register('users/me', UserViewSet)
# router.register('titles', TitleViewSet)
# router.register('categories', CategoryViewSet)
# router.register('genres', GenreViewSet)
# router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
# router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)', CommentViewSet, basename='comments')
# #/titles/{title_id}/reviews/{review_id}/
urlpatterns = [
    path('', include(router.urls)),
    #path('titles/', TitleViewSet.as_view()),
    #path('categories/', CategoryViewSet.as_view()),
    #path('genres/', GenreViewSet.as_view()),
    path('auth/email/', RegisterView.as_view()),
    path('auth/token/', ObtainAuthToken.as_view())
]