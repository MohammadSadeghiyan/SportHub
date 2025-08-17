from rest_framework.routers import SimpleRouter
from .views import ReceptionistViewSet

app_name='receptionists'

router=SimpleRouter()
router.register('receptionists',ReceptionistViewSet,'receptionist')

urlpatterns=router.urls