from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

REPORT_PARAMS=[ OpenApiParameter(name='name__iexact', description='name of report iexact',location=OpenApiParameter.QUERY, 
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