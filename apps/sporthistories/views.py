from rest_framework import viewsets,permissions
from .models import SportHistory
from .serializers import SportHistorySerializer
from .permissions import ManagerOrReceptionOrSelfCoachOrSelfAthlete
from .filters import SportHistoryFilter
from drf_spectacular.utils import extend_schema
from apps.athletes.models import Athlete
from .api_params import SPORT_HISTORY_PARAMS
@extend_schema(
    parameters=SPORT_HISTORY_PARAMS
)
class SportHistoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return super().get_queryset()
    
    serializer_class=SportHistorySerializer
    filterset_class=SportHistoryFilter
    permission_classes=[permissions.IsAuthenticated,ManagerOrReceptionOrSelfCoachOrSelfAthlete]
    lookup_field='public_id'


    def perform_create(self, serializer):
        user=self.request.user
        if user.role=='athlete':
            athlete= Athlete.objects.get(public_id=user.public_id)
            serializer.instance=SportHistory.objects.create(**serializer.validated_data,athlete=athlete)
        else:
            serializer.instance=SportHistory.objects.create(**serializer.validated_data)

        
    def perform_update(self, serializer):
        instance=self.get_object()
        if instance.status=='s':
            coach=instance.coach
            athlete=instance.athlete
            #need to add feature
                      
        
    
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    

