from rest_framework.routers import SimpleRouter
from .views import CoachViewSet

router=SimpleRouter()
router.register('coaches',CoachViewSet,'coach')

urlpatterns=router.urls
