from rest_framework import permissions

class ManagerOrSelfRecptionist(permissions.BasePermission):

    def has_permission(self, request, view):
        user=request.user
        if user.role in ['receptionist','manager']:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.role=='manager':
            return True
        return request.user.public_id==obj.user.public_id
    

class ManagerOrRecptionistOrSelfCoach(permissions.BasePermission):

    def has_permission(self, request, view):
        user=request.user
        if user.role=='manager' and request.method in permissions.SAFE_METHODS:
            return True
        if user.role in ['receptionist','coach']:
            return True
        return False
    
    
    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.role=='manager' and request.method in permissions.SAFE_METHODS:
            return True
        if request.role=='receptionist':
            return True
        return request.user.public_id==obj.user.public_id
    
    