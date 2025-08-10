from rest_framework import permissions
from .models import Coach
class IsSuperOrManagerOrCoach(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        return user.is_superuser or user.role=='manager'or( user.role=='Coach' and user.username==obj.username)