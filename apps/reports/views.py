from .models import Report
from .serializers import ReportSerializer
from rest_framework import viewsets,permissions
from .permissions import IsSuperOrReportManager
from .services import ReportService
from apps.managers.models import Manager
class ReportViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.is_superuser:
            return Report.objects.all()
        manager=Manager.objects.filter(pk=user.pk).first()
        return manager.reports.all()
    
    serializer_class=ReportSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrReportManager]

    def perform_create(self, serializer):
        user=self.request.user

        report_service=ReportService(serializer.validated_data,user)
        serializer.instance=report_service.make_report()
        

    def perform_update(self, serializer):
        instance=self.get_object()
        user=self.request.user
        report_service=ReportService(serializer.validated_data,user)
        serializer.instance=report_service.update_report(instance)
       

    
