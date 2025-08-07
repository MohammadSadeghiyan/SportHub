from django.db import models
from .helpers import date_validator
# Create your models here.

class Report(models.Model):
    TYPE_CHOICE=[
        ('year','YEAR'),
        ('month','Month'),
        ('day','Day')
    ]
    name=models.CharField(max_length=100)
    type_name=models.CharField(max_length=5,choices=TYPE_CHOICE)
    start_date=models.DateField(blank=True,validators=[date_validator])
    end_date=models.DateField(validators=[date_validator])
    total_sale=models.DecimalField(max_digits=15,decimal_places=0)
    total_payment=models.DecimalField(max_digits=15,decimal_places=0)
    total_reserve=models.PositiveIntegerField()
    active_user=models.PositiveIntegerField()
    inactive_user=models.PositiveIntegerField()
    expired_user=models.PositiveIntegerField()

    def __str__(self):
        return f'{self.pk}_{self.type}'