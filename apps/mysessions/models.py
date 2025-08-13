from django.db import models
from shortuuidfield import ShortUUIDField
# Create your models here.

class Mysession(models.Model):
    DAY_CHOICES=[
        ('even','Even'),
        ('odd','Odd'),
        ('all','All')
    ]
    public_id=ShortUUIDField(editable=False,unique=True)
    days_of_week=models.CharField(max_length=4,choices=DAY_CHOICES)
    start_time=models.TimeField()
    end_time=models.TimeField()

    def __str__(self):
        return f'{self.pk}_{self.days_of_week}'
