from rest_framework.routers import SimpleRouter
from .views import ReportViewSet
from rest_framework_nested.routers import NestedSimpleRouter
app_name='reports'
router=SimpleRouter()
router.register('reports',ReportViewSet,basename='report')
urlpatterns=router.urls