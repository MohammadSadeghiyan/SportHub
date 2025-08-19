from rest_framework.routers import SimpleRouter
from .views import ReservationViewSet

app_name='reservations'

router=SimpleRouter()
router.register('reservations',ReservationViewSet,'reservation')

urlpatterns=router.urls