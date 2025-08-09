from django.core.exceptions import ValidationError
import re
import os

def validate_iran_home_phone(value):
    pattern = r'^0\d{2}\d{8}$'
    if not re.match(pattern, str(value)):
        raise ValidationError({'home_number':'this home number is not true'})
    
def upload_to_role_based_path(instance,filename):
    _,extenstion=os.path.splitext(filename)
    if instance.username :
        return f"images/profile/{instance.role}/{instance.username}{extenstion}"
    return f"images/profile/{instance.role}/{filename}"

