from rest_framework import permissions

class ManagerReceptionReadOnlyOrAthlete(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role in['manager','receptionist'] and request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.role=='athlete':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        if request.user.role=='athlete':
            return obj.user.public_id==request.user.public_id
        return False
        
        
        


class ManagerReceptionReadOnlyOrCoach(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role in['manager','receptionist'] and request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.role=='coach':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        if request.user.role=='coach':
            return obj.user.public_id==request.user.public_id
        
        return False
        
        
class ManagerReceptionistReadOnlyOrUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role in ['manager','receptionist'] and request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role in['coach','athlete']:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist'] :
            return True
        else :return obj.order.user.public_id==request.user.public_id