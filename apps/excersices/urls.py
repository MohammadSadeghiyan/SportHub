from rest_framework.routers import SimpleRouter
from .views import *
app_name='excersices'

router=SimpleRouter()
router.register('excersices',ExcersiceViewSet,'excersice')

router.register('excersice-histories',ExcersiceHistoryViewSet,'excersice-history-detail')

urlpatterns=router.urls
