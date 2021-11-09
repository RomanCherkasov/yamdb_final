from rest_framework import permissions
from users.models import User


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == User.ADMIN
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class AdminOrModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == User.ADMIN
                or request.user.role == User.MODERATOR
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
