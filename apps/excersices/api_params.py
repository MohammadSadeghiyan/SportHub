from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

EXCERSICE_PARAMS=[ OpenApiParameter(name='include', description='Include related fields',location=OpenApiParameter.QUERY,
                                                 required=False, type=str,enum=['history']),
        OpenApiParameter(name='end_date', description='date of ending report time(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_date__gte', description='date of ending excersice time is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_date__lte', description='date of ending excersice time is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_date', description='date of start excersice (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_date__gte', description='date of start excersice is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_date__lte', description='date of start excersice is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='sport_history', description='uuid of sport history related to the excersice'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.UUID)
    ]

EXCERSICE_HISTORY_PARAMS=[
    OpenApiParameter(name='excersice', description='public_id of excersice iexact',location=OpenApiParameter.QUERY, 
                         required=False, type=OpenApiTypes.UUID),
       
    OpenApiParameter(name='description_icontains', description='description of report excersice history contain'
                          ,location=OpenApiParameter.QUERY,required=False, type=str), 
        
]