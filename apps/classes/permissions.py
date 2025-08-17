from rest_framework import permissions


class ManagerOrRecptionistOrCoachOrAthleteReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user=request.user
        if user.role in ['manager','receptionist','coach'] :
            return True
        elif user.role=='athlete'and request.method in permissions.SAFE_METHODS:
            return True
        
    
    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.role in ['manager','receptionist','athlete']:
            return True
        if user.role=='coach' and obj.coach.public_id==user.public_id:
            return True
        if user.role=='coach' and request.method in permissions.SAFE_METHODS:
            return True
       