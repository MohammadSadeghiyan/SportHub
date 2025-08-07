
from rest_framework import permissions

class IsSuperOrReportManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser and request.method in ['POST','PUT','PATCH']:
            return False
        user=request.user
        return user.is_superuser or user.role=='manager'
    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.is_superuser:
            return True
        if obj.managers.filter(username=user.username):
            return True
        return False
        
        
