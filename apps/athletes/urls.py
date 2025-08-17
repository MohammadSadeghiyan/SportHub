from rest_framework.routers import SimpleRouter
from .views import AthleteViewSet

app_name='athletes'

router=SimpleRouter()
router.register('athletes',AthleteViewSet,'athlete')

urlpatterns=router.urls