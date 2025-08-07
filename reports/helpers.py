from users.models import MidUser
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework.validators import ValidationError
def set_start_date(end_date,type_name):
    if type_name=='day':start_date=end_date-relativedelta(days=1)
    elif type_name=='month':start_date=end_date-relativedelta(months=1)
    elif type_name=='month':start_date=end_date-relativedelta(years=1)
    else : raise ValidationError('your type name is not validate')
    return start_date
def find_first_user_date_joined():
    if MidUser.objects.exists():
        return MidUser.objects.order_by('date_joined').first().date_joined.date()
    return timezone.now().date()

def date_validator(value):
    min_date = find_first_user_date_joined()
    if value < min_date:
        raise ValidationError({'min_date':f'your date must be after of {min_date}'})
    max_date = timezone.now().date()
    if value>max_date:
        raise ValidationError({'max_date':f'your date must be before of {max_date}'})
    
