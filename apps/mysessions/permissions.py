from rest_framework import permissions

class ManagerOrRecptionistOrCoachReadOnlyOrAthleteReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user=request.user
        if user.role in ['receptionist','manager']:
            return True
        elif user.role in ['coach','athlete'] and request.method in permissions.SAFE_METHODS:
            return True
    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.role in ['receptionist','manager']:
            return True
        return True