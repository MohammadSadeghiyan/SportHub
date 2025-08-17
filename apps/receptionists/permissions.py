from rest_framework import permissions


class IsManagerOrRecptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if user.role=='manager':
            return True
        if user.role=='receptionist' and request.method!='DELETE':
            return True
    def has_object_permission(self, request, view, obj):
        return request.user.role=='manager' or (request.user.role=='receptionist' and obj.username==request.user.username) 