from rest_framework import permissions,viewsets
from .permissions import AthleteOrCoachOrManagerOrRecptionist,AthleteOrCoachReadOnlyOrReceptionistOrManager
from .filters import PlanFilter,MealFilter
from .models import NutritionPlan,Meal
from .serializers import NutritionPlanSerializer,MealSerializer
from .helpers import nutritionplan_only_fields,meal_only_fields
from .services import NutritionplanService,MealService
from drf_spectacular.utils import extend_schema
from .api_params import MEAL_PARAMS

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
      
           
@extend_schema(
    parameters=MEAL_PARAMS
)
class MealViewSet(viewsets.ModelViewSet):


    def get_queryset(self):
        if self.request.user.role in ['manager','receptionist']:
            return Meal.objects.all().select_related('nutrition_plan').only(*meal_only_fields())
        elif self.request.user.role=='athlete':
            return Meal.objects.filter(nutrition_plan__athlete__public_id=self.request.user.public_id).select_related('nutrition_plan')\
                                    .only(*meal_only_fields)
        
        elif self.request.user.role=='coach':
            Meal.objects.filter(nutrition_plan__coach__public_id=self.request.user.public_id).select_related('nutrition_plan')\
                                    .only(*meal_only_fields)
        

        


    serializer_class=MealSerializer
    lookup_field='public_id'
    filterset_class=MealFilter
    permission_classes=[permissions.IsAuthenticated,AthleteOrCoachReadOnlyOrReceptionistOrManager]

    

    def perform_update(self, serializer):
        MealService.update(serializer,self.get_object())
    

    def perform_destroy(self, instance):
        MealService.delete(instance)