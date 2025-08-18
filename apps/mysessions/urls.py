from .views import MySessionViewSet
from rest_framework.routers import SimpleRouter

app_name='mysessions'

router=SimpleRouter()
router.register('sessions',MySessionViewSet,'session')

urlpatterns=router.urls