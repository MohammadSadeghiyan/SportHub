from django.utils import timezone
from apps.basicusers.models import MidUser
from django.core.exceptions import ValidationError
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
    
def start_date_validator(value):

    min_date = find_first_user_date_joined()
    if value < min_date:
        raise ValidationError({'min_date':f'your date must be after of {min_date}'})
