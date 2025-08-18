from rest_framework import permissions

class ReceptionsitOrAthleteOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role=='coach':
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        return request.user.public_id==obj.user.public_id
    

class ReceptionsitOrCoachOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role=='athlete':
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        return request.user.public_id==obj.user.public_id