from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.coaches.models import Coach
from apps.receptionists.models import Receptionist
from apps.athletes.models import Athlete
from sporthub.settings import MEDIA_ROOT
import os
from django.contrib.auth import get_user_model
from .helpers import check_file_name_exsit_with_any_extnestion,delete_file_with_exact_base_name
from django.conf import settings

User = get_user_model()
@receiver(post_save, sender=User)
def assign_admin_role_to_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
       instance.role='admin'
       instance.save()
       return


@receiver(post_save,sender=Coach)
@receiver(post_save,sender=Athlete)
@receiver(post_save,sender=Receptionist)
def set_image_name_base_username(sender,instance,**kwargs):
        
        if hasattr(instance, '_saving_from_signal') and instance._saving_from_signal:
            return
        instance._saving_from_signal = True
        if instance.image:
            image_relative_path_without_name=f'images/profile/{instance.role}'
            old_path=instance.image.path
            image_full_name=os.path.basename(instance.image.name)
            root, extension = os.path.splitext(image_full_name)
            if instance.username==root :
                if not check_file_name_exsit_with_any_extnestion(os.path.join(MEDIA_ROOT,image_relative_path_without_name),root,extension):
                    return
                else :
                     delete_file_with_exact_base_name(os.path.join(MEDIA_ROOT,image_relative_path_without_name),root,extension)
            else :
                print('ll')
                if not check_file_name_exsit_with_any_extnestion(os.path.join(MEDIA_ROOT,image_relative_path_without_name),instance.username):
                    print('nn')
                   
                else : 
                     print('mm')
                     delete_file_with_exact_base_name(os.path.join(MEDIA_ROOT,image_relative_path_without_name),instance.username,extension)
                new_image_full_name=instance.username+extension
                new_path = os.path.join(MEDIA_ROOT,image_relative_path_without_name, new_image_full_name)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.rename(old_path, new_path)
                instance.image.name=os.path.join(image_relative_path_without_name,new_image_full_name)
                instance.save(update_fields=['image'])