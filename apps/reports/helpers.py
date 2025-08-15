from apps.basicusers.models import MidUser
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework.validators import ValidationError
def set_start_date(end_date,type_name):
    if type_name=='day':start_date=end_date-relativedelta(days=1)
    elif type_name=='month':start_date=end_date-relativedelta(months=1)
    elif type_name=='year':start_date=end_date-relativedelta(years=1)
    else : raise ValidationError('your type name is not validate')
    return start_date
