from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAuthorOrReadOnly(BasePermission):
    """Только автор отзыва (комментария) может его редактировать."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'moderator'
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        try:
            if request.user.is_authenticated:
                return bool(
                    request.user.role == 'admin'
                    or request.user.is_superuser
                )
            return False
        except User.DoesNotExist:
            raise Http404


class IsUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
