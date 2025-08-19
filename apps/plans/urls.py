from rest_framework.routers import SimpleRouter
from .views import NutritionPlanViewSet,MealViewSet

app_name='plans'

router=SimpleRouter()
router.register('nutritionplans',NutritionPlanViewSet,'nutritionplan')
router.register('meals',MealViewSet,'meal')

urlpatterns=router.urls