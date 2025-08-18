from rest_framework.routers import SimpleRouter
from .views import MyMessageViewSet

app_name='mymessages'

router=SimpleRouter()
router.register('messages',MyMessageViewSet,'message')

urlpatterns=router.urls