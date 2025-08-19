from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

MEAL_PARAMS = [
    OpenApiParameter(
        name='athlete',
        description='Public ID of athlete',
        required=False,
        type=OpenApiTypes.UUID,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='athlete_date_done',
        description='Exact date when athlete marked meal as done (Jalali/Shamsi date)',
        required=False,
        type=OpenApiTypes.DATE,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='athlete_date_done__gte',
        description='Filter meals with athlete_date_done >= this date (Jalali/Shamsi date)',
        required=False,
        type=OpenApiTypes.DATE,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='athlete_date_done__lte',
        description='Filter meals with athlete_date_done <= this date (Jalali/Shamsi date)',
        required=False,
        type=OpenApiTypes.DATE,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='meal_discription',
        description='Search meal description (icontains)',
        required=False,
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='athlete_discription',
        description='Search athlete description (icontains)',
        required=False,
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='athlete_done',
        description='Filter by completion status (true/false)',
        required=False,
        type=OpenApiTypes.BOOL,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='day',
        description='Filter by day of week (saturday, sunday, ...)',
        required=False,
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
    ),
    OpenApiParameter(
        name='meal_type',
        description='Filter by type of meal (breakfast, lunch, dinner)',
        required=False,
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
    ),
]
