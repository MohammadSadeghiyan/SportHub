from rest_framework import permissions

class ManagerOrReceptionOrSelfCoachOrSelfAthlete(permissions.BasePermission):

    def has_permission(self, request, view):
        user=request.user
        if user.role=='manager' and request.method in permissions.SAFE_METHODS:
            return True
        elif user.role!='manager':return True
    
    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.role=='manager':
            return True
        elif user.role=='receptionist':
            return True
        elif user.role=='coach' and obj.coach.public_id==user.coach.public_id:
            return True
        elif user.role=='athlete' and obj.athlete.public_id==user.athlete.public_id:
            return True
        return False
    