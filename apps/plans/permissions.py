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
    

class AthleteOrCoachReadOnlyOrReceptionistOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role in['coach','manager','receptionist'] and request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role=='athlete':
            return True    

    def has_object_permission(self, request, view, obj):
        return request.user.role in['manager','receptionist'] or request.user.public_id==obj.nutrition_plan.coach.public_id or \
                    request.user.public_id==obj.nutrition_plan.athlete.public_id