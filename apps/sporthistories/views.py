from rest_framework import viewsets,permissions
from .serializers import SportHistorySerializer
from .permissions import ManagerOrReceptionOrSelfCoachOrSelfAthlete
from .filters import SportHistoryFilter
from drf_spectacular.utils import extend_schema
from .api_params import SPORT_HISTORY_PARAMS
from .services import SportHistoryService
from .models import SportHistory
from .helpers import sport_history_queryset_only_fields
from apps.excersices.models import Excersice
from django.db.models import Prefetch

@extend_schema(
    parameters=SPORT_HISTORY_PARAMS
)
class SportHistoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        params = self.request.GET
        has_exercise = 'excersice' in params
        
        if user.role in ['receptionist', 'manager']:
            queryset = SportHistory.objects.all()
        elif user.role == 'coach':
            queryset = SportHistory.objects.filter(coach__public_id=user.public_id)
        else:
            queryset = SportHistory.objects.filter(athlete__public_id=user.public_id)
        
        queryset = queryset.select_related('athlete', 'coach').only(*sport_history_queryset_only_fields())
        
        if has_exercise:
            if user.role in ['receptionist', 'manager']:
                exercise_queryset = Excersice.objects.all()
            elif user.role == 'coach':
                exercise_queryset = Excersice.objects.filter(coach__public_id=user.public_id)
            else:
                exercise_queryset = Excersice.objects.filter(athlete__public_id=user.public_id)
            
            queryset = queryset.prefetch_related(
                Prefetch('excersices', queryset=exercise_queryset.only('public_id'))
            )
            queryset = queryset.only(*sport_history_queryset_only_fields('excersice'))
        
        return queryset

    serializer_class=SportHistorySerializer
    filterset_class=SportHistoryFilter
    permission_classes=[permissions.IsAuthenticated,ManagerOrReceptionOrSelfCoachOrSelfAthlete]
    lookup_field='public_id'


    def perform_create(self, serializer):
        SportHistoryService.create(serializer,self.request.user)
        
    def perform_update(self, serializer):
        instance=self.get_object()  
        if instance.status=='s':
            SportHistoryService.update(instance,serializer)
        else :return super().perform_update(serializer)
            
    
    def perform_destroy(self, instance):
        SportHistoryService.delete(instance)
    

