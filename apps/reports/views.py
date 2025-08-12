from .models import Report
from .serializers import ReportSerializer
from rest_framework import viewsets,permissions
from .permissions import IsSuperOrReportManager
from .services import ReportService
from .filters import ReportFilter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
@extend_schema( 
    parameters=[
        OpenApiParameter(name='name__iexact', description='name of report iexact',location=OpenApiParameter.QUERY, 
                         required=False, type=str),
       
        OpenApiParameter(name='name_icontains', description='name of report contains',location=OpenApiParameter.QUERY,
                          required=False, type=str),
       
        OpenApiParameter(name='type_name', description='type of report',location=OpenApiParameter.QUERY, required=False, 
                            type=str,enum=['day','month','year']),
        
        OpenApiParameter(name='end_date', description='date of ending report (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_date__gte', description='date of ending report  is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_date__lte', description='date of ending report  is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_date', description='date of start report (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_date__gte', description='date of start report  is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_date__lte', description='date of start report  is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

    ]
)

class ReportViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Report.objects.select_related('manager').filter(manager__public_id=self.kwargs['manager_public_id'])
    
    serializer_class=ReportSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrReportManager]
    lookup_field='public_id'
    filterset_class=ReportFilter
    def perform_create(self, serializer):
        report_service=ReportService(serializer.validated_data,self.kwargs['manager_public_id'])
        serializer.instance=report_service.make_report()
        

    def perform_update(self, serializer):
        instance=self.get_object()
        report_service=ReportService(serializer.validated_data,self.kwargs['manager_public_id'])
        serializer.instance=report_service.update_report(instance)
       

    
