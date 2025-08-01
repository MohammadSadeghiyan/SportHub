from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import MidUser
from sporthub.settings import MEDIA_ROOT
import os
@receiver(post_save,sender=MidUser)
def set_image_name_base_username(sender,instance,**kwargs):
        if instance.image:
            image_relative_path_without_name=f'images/profile/{instance.role}'
            old_path=instance.image.path
            image_full_name=os.path.basename(instance.image.name)
            root, extension = os.path.splitext(image_full_name)
            if instance.username==root:
                return
            else :
                new_image_full_name=instance.username+extension
                new_path = os.path.join(MEDIA_ROOT,image_relative_path_without_name, new_image_full_name)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.rename(old_path, new_path)
                instance.image.name=os.path.join(image_relative_path_without_name,new_image_full_name)
                instance.save(update_fields=['image'])