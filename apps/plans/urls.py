from rest_framework.routers import SimpleRouter
from .views import NutritionPlanViewSet

app_name='plans'

router=SimpleRouter()
router.register('nutritionplans',NutritionPlanViewSet,'nutritionplan')

urlpatterns=router.urls