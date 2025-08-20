from rest_framework.routers import SimpleRouter
from .views import SportHistoryViewSet

app_name='sporthistories'
router=SimpleRouter()
router.register('sport-histories',SportHistoryViewSet,'sport-history')

urlpatterns=router.urls