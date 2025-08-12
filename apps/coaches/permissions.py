from rest_framework import permissions
from .models import Coach
class IsManagerOrCoachOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if  user.role == 'athlete' and request.method in permissions.SAFE_METHODS :
            return True
        if user.role in ['receptionist','manager'] and (request.method in permissions.SAFE_METHODS or request.method=='POST') :
            return True
        elif user.role=='coach':
            return True
    

    def has_object_permission(self, request, view, obj):
        user=request.user
        return user.role=='manager'or user.role=='receptionist' or user.role=='athlete'or\
            ( user.role=='coach' and user.public_id==obj.public_id)