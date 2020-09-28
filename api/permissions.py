from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        message = 'Please, log in'
        is_auth = bool(request.user and request.user.is_authenticated)
        if is_auth:
            return is_auth
        else:
            raise PermissionDenied(detail=message)
