from django.db import models
from apps.basicusers.models import BaseUser
# Create your models here.

class Manager(BaseUser):
    def save(self, *args, **kwargs):
        self.role = 'manager'
        super().save(*args, **kwargs)
