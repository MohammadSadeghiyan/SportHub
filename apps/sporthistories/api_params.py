from drf_spectacular.utils import OpenApiParameter, OpenApiTypes


SPORT_HISTORY_PARAMS = [ OpenApiParameter(name='include', description='Include related fields',location=OpenApiParameter.QUERY
                         ,required=False, type=str,enum=['excersice']),
        OpenApiParameter(name='end_date', description='date of ending coopreation time(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_date__gte', description='date of ending coopreation is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_date__lte', description='date of ending coopreation is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_date', description='date of start coopreation (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_date__gte', description='date of start coopreation is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_date__lte', description='date of start coopreation is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='confirmation_coach', description='stauts of sport history coach confirmation'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.BOOL),
        OpenApiParameter(name='balance_for_coaching_rial', description='exact balance of sport history'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='balance_for_coaching_rial__range', description='range of balance of sport history'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='balance_for_coaching_rial__lte', description='balance of sport history is less than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='balance_for_coaching_rial__gte', description='balance of sport history is grater than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='status', description='stauts of sport history '
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.STR,enum=['not start','start']),
    ]