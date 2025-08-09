from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.routers import SimpleRouter
from apps.managers.views import ManagerViewSet
from apps.reports.views import ReportViewSet
from django.urls import path,include
router=SimpleRouter()
router.register('managers',viewset=ManagerViewSet,basename='manager')

manager_router=NestedSimpleRouter(router,'managers',lookup='manager')
manager_router.register('reports',ReportViewSet,basename='manager-reports')




urlpatterns=[
    path('',include(router.urls)),
    path('',include(manager_router.urls))
                  ]