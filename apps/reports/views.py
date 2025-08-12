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
        OpenApiParameter(name='name_iexact', description='name of report',location=OpenApiParameter.QUERY, 
                         required=False, type=str),
       
        OpenApiParameter(name='name_icontains', description='name of report',location=OpenApiParameter.QUERY,
                          required=False, type=str),
       
        OpenApiParameter(name='type', description='type of report',location=OpenApiParameter.QUERY, required=False, 
                            type=str,enum=['day','month','year']),
        
        OpenApiParameter(name='end_date', description='date of ending report time',location=OpenApiParameter.QUERY, required=False, 
                            type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_date_gte', description='date of ending report time is grater than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_date_lte', description='date of ending report time is less than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_date', description='date of start report time',location=OpenApiParameter.QUERY, required=False, 
                            type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_date_gte', description='date of start report time is grater than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_date_lte', description='date of start report time is less than or equal'
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
       

    
