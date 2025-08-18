from .models import Membership
from .serializers import AthleteMembershipSerializer,CoachMembershipSerializer
from .permissions import *
from .filters import MembershipFilter
from .helpers import MembershipOnlyfields
from rest_framework import viewsets,permissions
from .services import MembershipService



class AthleteMembershipViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.request.user.role in ['receptionist','manager']:
            return Membership.objects.all().select_related('user').only(*MembershipOnlyfields())
        return Membership.objects.filter(user__public_id=self.request.user.public_id).select_related('user')\
                .only(*MembershipOnlyfields())
 
    serializer_class=AthleteMembershipSerializer
    permission_classes=[permissions.IsAuthenticated,ReceptionsitOrAthleteOrManager]
    lookup_field='public_id'
    filterset_class=MembershipFilter

    def perform_create(self, serializer):
        user=self.request.user
        MembershipService.create(user,serializer)

    def perform_update(self, serializer):
        instance=self.get_object()
        MembershipService.update(self.request.user,instance,serializer)
    
    def perform_destroy(self, instance):
        
        MembershipService.delete(instance)


class CoachMembershipViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.request.user.role in ['receptionist','manager']:
            return Membership.objects.all().select_related('user').only(*MembershipOnlyfields())
        return Membership.objects.filter(user__public_id=self.request.user.public_id).select_related('user')\
                .only(*MembershipOnlyfields())
    
    lookup_field='public_id'
    permission_classes=[permissions.IsAuthenticated,ReceptionsitOrCoachOrManager]
    filterset_class=MembershipFilter
    serializer_class=CoachMembershipSerializer

    def perform_create(self, serializer):
        user=self.request.user
        MembershipService.create(user,serializer)
    
    def perform_update(self, serializer):
        instance=self.get_object()
        MembershipService.update(self.request.user,instance,serializer)   
    def perform_destroy(self, instance):
        MembershipService.delete(instance)
