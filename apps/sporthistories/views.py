from rest_framework import viewsets,permissions
from .models import SportHistory
from .serializers import SportHistorySerializer
from .permissions import ManagerOrReceptionOrSelfCoachOrSelfAthlete
from .filters import SportHistoryFilter
from drf_spectacular.utils import extend_schema
from apps.athletes.models import Athlete
from .api_params import SPORT_HISTORY_PARAMS
from django.utils import timezone


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
        else:
            athlete=serializer.validated_data.pop('athlete')
        
        serializer.instance=SportHistory.objects.create(**serializer.validated_data,athlete=athlete,status='ns')


        
    def perform_update(self, serializer):
        instance=self.get_object()
        user=self.request.user
        if instance.status=='s':
            if instance.end_date>timezone.now().date():    
                coach=instance.coach
                athlete=instance.athlete
                instance.status='c'
                instance.save()

                if instance.start_date >timezone.now().date():
                    salary=instance.balance_for_coaching_rial
                else:
                    time_delta=instance.end_date-timezone.now().date()
                    salary=instance.pricing.price_per_day*time_delta

                athlete.balance_rial+=salary
                athlete.save()
                coach.balance_rial-=salary
                coach.save()   

                new_athlete=serializer.validated_data.pop('athlete',instance.athlete)
                SportHistory.objects.create(**serializer.validated_date,athlete=new_athlete)

            else : pass

            
        # else :
        #     return super().perform_update(serializer)
            
                      
        
    
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    

