from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_staff


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Docstring."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.request.user.is_admin or self.request.user.is_staff


class IsModerator(permissions.BasePermission):
    """Docstring."""

    def has_object_permission(self, request, view, obj):
        return self.request.user.is_moderator


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ на изменение только авторам."""

    message = 'Изменения может вносить только автор!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
