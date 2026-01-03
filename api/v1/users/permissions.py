from rest_framework.permissions import BasePermission

from api.v1.users.models import CustomUser


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, CustomUser):
            if obj.is_staff:
                return True
            return request.user.id == obj.id
        elif hasattr(obj, 'user'):
            if obj.user.is_staff:
                return True
            return request.user.id == obj.user.id
        return False