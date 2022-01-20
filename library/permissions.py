from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на уровне объекта. Позволяет изменять и удалять объект только
    владельцу этого объекта
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.owner:
            return obj.owner == request.user
        else:
            return False
