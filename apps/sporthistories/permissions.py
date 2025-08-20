from rest_framework import permissions
from django.utils import timezone
class ManagerOrReceptionOrSelfCoachOrSelfAthlete(permissions.BasePermission):

    def has_permission(self, request, view):
        user=request.user
        if user.role=='manager' and request.method in permissions.SAFE_METHODS:
            return True
        elif user.role=='coach' and request.method!='POST':return True
        elif user.role not in['coach','manager']:return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj.status=='s' and obj.end_date<=timezone.now().date() and request.method in ['PUT',"PATCH",'DELETE']:
            return False
        user=request.user
        if user.role=='manager':
            return True
        elif user.role=='receptionist':
            return True
        elif user.role=='coach' and obj.coach.public_id==user.public_id:
            return True
        elif user.role=='athlete' and obj.athlete.public_id==user.public_id:
            return True
        return False
    