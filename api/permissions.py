from rest_framework import permissions
from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action is None:
            return True
        return (request.user.is_authenticated
                and request.user.role == User.ADMIN)


class FullAcessOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        role = (User.MODERATOR, User.ADMIN,)
        return request.user.role in role or obj.author == request.user
