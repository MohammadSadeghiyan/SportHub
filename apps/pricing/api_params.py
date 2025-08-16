from drf_spectacular.utils import OpenApiParameter, OpenApiTypes


CLASS_ITEM_PRICING_ITEMS = [ 
        OpenApiParameter(name='end_start_date', description='end date of start policy time(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_start_date__gte', description='end date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_start_date__lte', description='end date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_start_date', description='date of start policy (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_start_date__gte', description='date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_start_date__lte', description='date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='max_capacity__range', description='max capacity of class range'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='max_capacity', description='max capacity of class '
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='max_capacity__lte', description='max capacity of class less than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='max_capacity__gte', description='max capacity of class bigger than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
       OpenApiParameter(name='min_capacity__range', description='min capacity of class range'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='min_capacity', description='min capacity of class '
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='min_capacity__lte', description='min capacity of class less than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='min_capacity__gte', description='min capacity of class bigger than or equal'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='price_per_hour__range', description='range of price per hour range'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='session_ref', description='session id if class'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.UUID),
        OpenApiParameter(name='gym_fee__range', description='gym fee of class range'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
    ]


MEMBERSHIP_PRICING_ITEMS = [ 
        OpenApiParameter(name='end_start_date', description='end date of start policy time(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_start_date__gte', description='end date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_start_date__lte', description='end date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_start_date', description='date of start policy (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_start_date__gte', description='date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_start_date__lte', description='date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='price__range', description='range of price'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='price', description=' price'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='gym_fee__range', description='gym fee of class range'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='type_name', description='type of membership'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.STR ,enum=['year','month']),
    ]


NUTRITION_PRICING_ITEMS = [ 
        OpenApiParameter(name='end_start_date', description='end date of start policy time(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_start_date__gte', description='end date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_start_date__lte', description='end date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_start_date', description='date of start policy (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_start_date__gte', description='date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_start_date__lte', description='date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='price_per_day__range', description='range of price per day'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='price_per_day', description=' price per day'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='gym_fee__range', description='gym fee of class range'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        
    ]



SPORTHISTORY_PRICING_ITEMS = [ 
        OpenApiParameter(name='end_start_date', description='end date of start policy time(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_start_date__gte', description='end date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_start_date__lte', description='end date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_start_date', description='date of start policy (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_start_date__gte', description='date of start policy is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_start_date__lte', description='date of start policy is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='price_per_day__range', description='range of price per day'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='price_per_day', description=' price per day'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        OpenApiParameter(name='gym_fee__range', description='gym fee of class range'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.INT),
        
    ]