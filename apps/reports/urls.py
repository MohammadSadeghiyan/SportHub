from rest_framework.routers import SimpleRouter
from .views import ReportViewSet
app_name='reports'
router=SimpleRouter()
router.register('reports',ReportViewSet,'report')
urlpatterns=router.urls