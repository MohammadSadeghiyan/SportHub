from rest_framework import permissions

class IsCoachOrAthlete(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if user.role=='coach':
            return True
        elif user.role=='athlete':
            if request.method in ['GET','PUT',"PATCH"]:
                return True
            return False
        return False
    def has_object_permission(self, request, view, obj):
        return obj.sport_history.coach.username==request.user.username or obj.sport_history.athlete.username==request.user.username