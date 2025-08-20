from rest_framework import viewsets,permissions
from .models import WorkHistory
from .serializers import *
from .filters import *
from .permissions import *
from .helpers import *
from apps.receptionists.models import Receptionist
class ReceptionistWorkHistoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.role in 'manager':
            return WorkHistory.objects.all().select_related('user').only(*get_work_history_only_fields())
        else: 
            other_receptions_id=Receptionist.objects.exclude(public_id=user.public_id).values_list('public_id',flat=True)
            return WorkHistory.objects.exclude(user__role='receptionist',user__public_id__in=other_receptions_id)\
                                        .select_related('user').only(*get_work_history_only_fields())
  
    
    lookup_field="public_id"
    filterset_class=WorkHistoryFilter
    serializer_class=ReceptionistWorkHistorySerializer
    permission_classes=[permissions.IsAuthenticated,ManagerOrSelfRecptionist]
    
    def perform_create(self, serializer):
        user=self.request.user
        if user.role=='manager':
            return super().perform_create(serializer)
        receptionist=Receptionist.objects.get(public_id=user.public_id)
        serializer.instance= WorkHistory.objects.create(**serializer.validated_data,user=receptionist)

   
    def perform_update(self, serializer):
        user=self.request.user
        if user.role=='manager':
            return super().perform_update(serializer)
        receptionist=Receptionist.objects.get(public_id=user.public_id)
        for attr, value in serializer.validated_data.items():
            setattr(receptionist, attr, value) 
        receptionist.save()
        serializer.instance=receptionist
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    

class CoachWorkHistoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptionist']:
            return WorkHistory.objects.all().select_related('user').only(*get_work_history_only_fields())
        else: 
            return WorkHistory.objects.exclude(user__public_id=user.public_id)\
                                        .select_related('user').only(*get_work_history_only_fields())
  
    
    lookup_field="public_id"
    filterset_class=WorkHistoryFilter
    serializer_class=CoachWorkHistorySerializer
    permission_classes=[permissions.IsAuthenticated,ManagerOrRecptionistOrSelfCoach]

    def perform_create(self, serializer):
        user=self.request.user
        if user.role in['manager','receptionist']:
            return super().perform_create(serializer)
        coach=Coach.objects.get(public_id=user.public_id)
        serializer.instance= WorkHistory.objects.create(**serializer.validated_data,user=coach)
    
    def perform_update(self, serializer):
        user=self.request.user
        if user.role in['receptionist','manager']:
            return super().perform_update(serializer)
        coach=Coach.objects.get(public_id=user.public_id)
        for attr, value in serializer.validated_data.items():
            setattr(coach, attr, value) 
        coach.save()
        serializer.instance=coach
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    