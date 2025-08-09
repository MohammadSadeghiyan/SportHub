from django.db import models
from apps.coaches.models import Coach
from apps.mysessions.models import Mysession
# Create your models here.


class Class(models.Model):
    name=models.CharField(max_length=100)
    session=models.ForeignKey(Mysession,on_delete=models.SET_NULL,null=True,related_name='classes')
    start_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    end_date=models.DateField()
    capacity=models.PositiveSmallIntegerField()
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='classes')
    class_salary_get_per_athlete_rial=models.DecimalField(max_digits=9,decimal_places=0)

    @property
    def get_full_price(self):
        if self.pk:
            athlete_registered=self.reserves.filter(status='ack')
            total=0
            for athlete in athlete_registered:
                total+=athlete.salary_rial*.9
            return total
        
    
    def __str__(self):
        return f'{self.name}_{self.capacity}'
