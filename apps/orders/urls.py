from .views import *
from rest_framework.routers import SimpleRouter

app_name='orders'

router=SimpleRouter()
router.register('sporthistory-items',SportHistoryItemViewSet,'sporthistory-item')
router.register('membership-itmes',MembershipItemViewSet,'membership-item')
router.register('nutritionplan-items',NutritionPlanItemViewSet,'nutrition-plan-item')
router.register('reservation-items',ReservationItemViewSet,'reservation-item')
router.register('athlete-orders',AthleteOrderViewSet,'athlete-order')
router.register('coach-orders',CoachOrderViewSet,'coach-order')

urlpatterns=router.urls