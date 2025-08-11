from rest_framework import permissions


class IsSuperOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if request.method in ['PUT','PATCH','DELETE']  and user.is_superuser:
            return False
        return user.role=='manager' or user.is_superuser
    def has_object_permission(self, request, view, obj):
        return (request.user.role=='manager' and obj.public_id==request.user.public_id) or request.user.is_superuser
