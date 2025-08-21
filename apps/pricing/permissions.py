from rest_framework import permissions

class ManagerNoUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT','PATCH']:
            return False
        if request.user.role=='manager':
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.role=='manager':
            return True
        return False
    
class ManagerNoCreatePermissionOrReceptionistReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            return False
        if request.user.role=='manager':
            return True
        if request.user.role=='receptionist' and request.method in permissions.SAFE_METHODS:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.role in['manager','receptionist']:
            return True
        return False
    

class ManagerOrReceptionistReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role=='receptionist' and request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role=='manager':
            return True
        return False    
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        return False