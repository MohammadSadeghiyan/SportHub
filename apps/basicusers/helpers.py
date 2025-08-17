from django.core.exceptions import ValidationError
import re
import os
from sporthub.settings import MEDIA_ROOT

def validate_iran_home_phone(value):
    pattern = r'^0\d{2}\d{8}$'
    if not re.match(pattern, str(value)):
        raise ValidationError({'home_number':'this home number is not true'})
    
def upload_to_role_based_path(instance,filename):
    _,extenstion=os.path.splitext(filename)
    print(filename)
    if instance.username and not check_file_name_exsit_with_any_extnestion(os.path.join(MEDIA_ROOT,'images','profile',instance.role)
                                                                           ,instance.username,extenstion):
        return f"images/profile/{instance.role}/{instance.username}{extenstion}"
    return f"images/profile/{instance.role}/{filename}"

def check_file_name_exsit_with_any_extnestion(directory_path, file_base_name,base_extension=None):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    for filename in os.listdir(directory_path):
        name, extension= os.path.splitext(filename)
        if name == file_base_name :
            if base_extension:
                if base_extension!=extension:
                    return True
                return False
            return True
    return False



def delete_file_with_exact_base_name(directory_path, file_base_name,base_extension=None):
    if not os.path.exists(directory_path):
          return
    for filename in os.listdir(directory_path):
        name, extension= os.path.splitext(filename)
        if name == file_base_name :
            if base_extension:
                if base_extension!=extension:
                    os.remove(os.path.join(directory_path,filename)) 
                continue
            os.remove(os.path.join(directory_path,filename)) 


