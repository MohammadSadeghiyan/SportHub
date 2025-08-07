from .models import Report
from .serializers import ReportSerializer
from rest_framework import viewsets,permissions
from .permissions import IsSuperOrReportManager
from users.models import Manager
from .services import make_report,update_report
from .helpers import set_start_date
from users.models import Manager
class ReportViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.is_superuser:
            return Report.objects.all()
        manager=Manager.objects.filter(pk=user.pk).prefetch_related('reports').first()
        return manager.reports.all()
    
    serializer_class=ReportSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrReportManager]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.instance=make_report(serializer.validated_data,user)
        

    def perform_update(self, serializer):
        instance=self.get_object()
        user=self.request.user
        serializer.instance=update_report(serializer.validated_data,instance,user)

       

    
