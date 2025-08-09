from django.db import models
from apps.athletes.models import Athlete
from apps.coaches.models import Coach
# Create your models here.

class SportHistory(models.Model):
    athlete=models.ForeignKey(Athlete,on_delete=models.CASCADE,related_name='sport_historys')
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='users_coaching')
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(null=True,blank=True)
    confirmation_coach=models.BooleanField(default=False)
    balance_for_coaching_rial=models.DecimalField(verbose_name='balance for coaching(rial)',max_digits=12,decimal_places=0)


  
    def __str__(self):
        return f'{self.athlete.username}_{self.coach.username}_{self.start_date}'
