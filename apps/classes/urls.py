from .views import ClassViewSet
from rest_framework.routers import SimpleRouter

app_name='classes'

router=SimpleRouter()
router.register('classes',ClassViewSet,'class')

urlpatterns=router.urls