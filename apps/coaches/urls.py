from rest_framework.routers import SimpleRouter
from .views import CoachViewSet
app_name='coaches'
router=SimpleRouter()
router.register('coaches',CoachViewSet,'coach')

urlpatterns=router.urls
