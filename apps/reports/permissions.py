
from rest_framework import permissions

class IsSuperOrReportManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return  user.role=='manager'
    def has_object_permission(self, request, view, obj):
        if obj.manager and obj.manager.public_id==request.user.public_id:
            return True
        return False
        
        
