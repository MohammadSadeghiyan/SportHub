from .models import Report
from .serializers import ReportSerializer
from rest_framework import viewsets,permissions
from .permissions import IsSuperOrReportManager
from .services import ReportService
class ReportViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Report.objects.filter(manager__pk=self.kwargs['manager_pk'])
    
    serializer_class=ReportSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrReportManager]
    lookup_url_kwarg = 'pk'
    def perform_create(self, serializer):
        report_service=ReportService(serializer.validated_data,self.kwargs['manager_pk'])
        serializer.instance=report_service.make_report()
        

    def perform_update(self, serializer):
        instance=self.get_object()
        report_service=ReportService(serializer.validated_data,self.kwargs['manager_pk'])
        serializer.instance=report_service.update_report(instance)
       

    
