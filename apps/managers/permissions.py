from rest_framework import permissions


class IsSuperOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return user.is_superuser or user.role=='manager'
    def has_object_permission(self, request, view, obj):
        return (request.user.role=='manager' and obj.username==request.user.username) or request.user.is_superuser
