from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == 'GET': #permissions.SAFE_METHODS:
            return True
        print('!!!!!!!!!!!!!')
        print(request.user.is_authenticated)
        # if request.method == 'POST' and not request.user.is_authenticated:
        #     raise NotAuthenticated()
        return request.user.is_staff #request.user.username == 'admin'



