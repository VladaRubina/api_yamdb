from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Docstring."""

    def has_object_permission(self, request, view, obj):
        return self.request.user.is_admin


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
