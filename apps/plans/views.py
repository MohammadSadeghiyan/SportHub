from rest_framework import permissions,viewsets
from .permissions import AthleteOrCoachOrManagerOrRecptionist
from .filters import PlanFilter
from .models import NutritionPlan
from .serializers import NutritionPlanSerializer
from .helpers import nutritionplan_only_fields
from .services import NutritionplanService

class NutritionPlanViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.role in ['receptionist','manager']:
            return NutritionPlan.objects.all().select_related('athlete','coach').only(*nutritionplan_only_fields())
        if user.role=='athlete':
            return NutritionPlan.objects.filter(athlete__public_id=user.public_id)\
                    .select_related('athlete','coach').only(*nutritionplan_only_fields())
        return NutritionPlan.objects.filter(coach__public_id=user.public_id)\
                .select_related('athlete','coach').only(*nutritionplan_only_fields())
    
    serializer_class=NutritionPlanSerializer
    lookup_field='public_id'
    filterset_class=PlanFilter
    permission_classes=[permissions.IsAuthenticated,AthleteOrCoachOrManagerOrRecptionist]

    def perform_create(self, serializer):
        user=self.request.user
        NutritionplanService.create(user,serializer)
    
    def perform_update(self, serializer):
        instance=self.get_object()
        NutritionplanService.update(instance,serializer)
        
    def perform_destroy(self, instance):
        NutritionplanService.delete(instance)
      
           