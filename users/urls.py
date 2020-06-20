from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from users.views import RegisterView, ObtainAuthToken, UserViewSet
from django.views.decorators.csrf import csrf_exempt

user_routers = DefaultRouter()
user_routers.register('', UserViewSet)

urlpatterns = [
    #path('titles/', TitleViewSet.as_view()),
    #path('categories/', CategoryViewSet.as_view()),
    #path('genres/', GenreViewSet.as_view()),
    # path(r'users/me/', UserMeViews.as_view()),
    # path(r'users/<str:username>/', UserAdminViewSet.as_view()),
    # path(r'users/', UserAdminViewSet.as_view()),
    path('users/', include(user_routers.urls)),
    path('auth/email/', RegisterView.as_view()),
    path('auth/token/', ObtainAuthToken.as_view())
]
