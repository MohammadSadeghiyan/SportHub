from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.routers import SimpleRouter
from apps.managers.views import ManagerViewSet
from apps.reports.views import ReportViewSet
router=SimpleRouter()
router.register('managers',ManagerViewSet,'manager')
