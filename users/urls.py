from rest_framework.routers import SimpleRouter
from .views import *
app_name='users'
router=SimpleRouter()
router.register('managers',viewset=ManagerViewSet,basename='manager')
router.register('receptionists',viewset=ReceptionistViewSet,basename='receptionist')













urlpatterns=router.urls