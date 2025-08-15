from rest_framework.routers import SimpleRouter
from .views import *

app_name='pricing'

router=SimpleRouter()
router.register('class-pricing',ClassPricingViewSet,'classpricing')
router.register('class-item-pricing',ClassItemPricingViewSet,'classitempricing')
router.register('sporthistory-pricing',SportHistoryPricingViewSet,'sporthistorypricing')
router.register('membership-pricing',MembershipPricingViewSet,'membershippricing')
router.register('nutrition-pricing',NutritionPricingViewSet,'nutritionpricing')

urlpatterns=router.urls