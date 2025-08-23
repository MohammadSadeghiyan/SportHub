from rest_framework import permissions

class ManagerOrAthleteOrReceptionist(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role in ['manager','receptionist','athlete'] :
            return True
        return False
    

    def has_object_permission(self, request, view, obj):
        if request.user.role =='manager':
            return True
        if request.user.public_id==obj.reserved_by.public_id:
            return True
        return False