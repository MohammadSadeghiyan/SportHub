from .views import *
from rest_framework.routers import SimpleRouter

app_name='memberships'

router=SimpleRouter()
router.register('athlete-memberships',AthleteMembershipViewSet,'athlete-membership')
router.register('coach-memeberships',CoachMembershipViewSet,'coach-membership')

urlpatterns=router.urls