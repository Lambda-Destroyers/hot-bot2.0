from rest_framework import permissions
from .models import HotBot

class isOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, HotBot):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return obj.owner == request.user
