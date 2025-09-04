from rest_framework import permissions


class IsActive(permissions.BasePermission):
    """Проверяем входит пользователь в группу модераторов."""

    def has_permission(self, request, view):
        return request.user and request.user.is_active
