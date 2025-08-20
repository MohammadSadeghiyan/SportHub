from rest_framework import permissions

class SenderOrReciverOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.role=='manager' :
            return True
        if request.user.public_id==obj.reciver.public_id and request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.public_id==obj.sender.public_id:
            return True
    