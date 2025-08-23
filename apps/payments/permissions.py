from rest_framework import permissions


class ManagerReceptionSelfUserReadOnly(permissions.BasePermission):

    

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        return request.user.public_id==obj.user.public_id
    

class ManagerOrReceptionistReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role=='manager':
            return True
        elif request.user.role=='receptionist' and request.method in permissions.SAFE_METHODS:
            return True
        return False
    

    def has_object_permission(self, request, view, obj):
        if request.user.role=='manager':
            return True
        if request.user.role=='receptionist':
            return obj.user.public_id==request.user.public_id
        return False
    

class ManagerOrReceptionistOrSelfUser(permissions.BasePermission):

    

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        else :
            if request.method in permissions.SAFE_METHODS:
                return obj.user.public_id==request.user.public_id
            return False