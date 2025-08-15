from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.routers import SimpleRouter
from apps.managers.views import ManagerViewSet
from apps.reports.views import ReportViewSet
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router=SimpleRouter()
router.register('managers',viewset=ManagerViewSet,basename='manager')

manager_router=NestedSimpleRouter(router,'managers',lookup='manager')
manager_router.register('reports',ReportViewSet,basename='manager-reports')




urlpatterns=[
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/',include('apps.coaches.urls')),
    path('api/',include('apps.excersices.urls')),
    path('api/',include('apps.sporthistories.urls')),
    path('api/',include('apps.workhistories.urls')),
    path('api/',include(router.urls)),
    path('api/',include(manager_router.urls)),
    path('api/',include('apps.pricing.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
   
                  