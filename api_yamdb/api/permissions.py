from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ к небезопасным методам только для админа(модели Title, Category, Genre)."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Docstring."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.request.user.is_admin or self.request.user.is_staff


class IsAuthorModeratorOrReadOnly(permissions.BasePermission):
    """Доступ на изменение только авторам."""

    message = 'Изменения доступны только авторам или модераторам!'
   
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_moderator


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Доступ на изменение только авторам."""

    message = 'Изменения доступны только авторам, модераторам или админам!'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
