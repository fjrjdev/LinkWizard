from rest_framework import permissions
import ipdb


class IsAdminOwnerLink(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.user.id == request.user.id:
            return True
        return False
