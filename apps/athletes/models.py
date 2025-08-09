from django.db import models
from apps.coaches.models import Coach
from apps.basicusers.models import MidUser
# Create your models here.

class Athlete(MidUser):
    classes=models.ManyToManyField('classes.Class',blank=True,related_name='athletes')
    coachs=models.ManyToManyField(Coach,through='sporthistories.SportHistory',related_name='athletes',blank=True)
    weight=models.PositiveSmallIntegerField(default=0)
    height=models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.role = 'athlete'
        super().save(*args, **kwargs)