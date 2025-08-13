from rest_framework.routers import SimpleRouter
from .views import *

app_name='workhistories'

router=SimpleRouter()
router.register('receptionists-workhistories',ReceptionistWorkHistoryViewSet,'receptionist-workhistory')
router.register('coaches-workhistories',CoachWorkHistoryViewSet,'coach-workhistory')

urlpatterns=router.urls