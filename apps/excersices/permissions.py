from rest_framework import permissions

class IsCoachOrAthleteExcersiceOrManagerReceptionistReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if user.role=='manager' and request.method in permissions.SAFE_METHODS:return True
        elif user.role=='coach':
            return True
        elif user.role=='athlete':
            if request.method in ['PUT',"PATCH"] or request.method in permissions.SAFE_METHODS:
                return True
            return False
        return False
    def has_object_permission(self, request, view, obj):
        user=request.user
        return user.role=='manager' or obj.sport_history.coach.public_id==user.public_id or obj.sport_history.athlete.public_id==user.public_id
    

class IsCoachOrAthleteHistory(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if user.role in ['coach','manager','receptionist']and request.method in permissions.SAFE_METHODS:
            return True
        elif user.role=='athlete':
            return True
    
    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.role=='manager':
            return True
        elif user.role=='athlete':
            return user.public_id==obj.excersice.sport_history.athlete.public_id
        return user.public_id==obj.excersice.sport_history.coach.public_id