from rest_framework import permissions

class AthleteOrCoachOrManagerOrRecptionist(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role =='coach' :
            if request.method!='POST':
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['manager','receptionist']:
            return True
        
        return obj.athlete.public_id==request.user.public_id or obj.coach.public_id==request.user.public_id
    