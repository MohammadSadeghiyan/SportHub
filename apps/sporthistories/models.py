from django.db import models
from apps.athletes.models import Athlete
from apps.coaches.models import Coach
from shortuuidfield import ShortUUIDField
from django.core.validators import MinValueValidator
from apps.pricing.models import SportHistoryPricing
from django.core.exceptions import ValidationError
from apps.pricing.models import SportHistoryPricing
# Create your models here.

class SportHistory(models.Model):
    STATUS_CHOICES=(
        ('r','registered'),
        ('nr','not registered'),
        ('c','cancel')
    )
    status=models.CharField(max_length=2,choices=STATUS_CHOICES)
    public_id=ShortUUIDField(editable=False,unique=True)
    athlete=models.ForeignKey(Athlete,on_delete=models.CASCADE,related_name='sport_histories')
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='sport_histories')
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(null=True,blank=True)
    confirmation_coach=models.BooleanField(default=False)
    balance_for_coaching_rial=models.DecimalField(verbose_name='balance for coaching(rial)',max_digits=12,decimal_places=0,
                                                  validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f'{self.athlete.username}_{self.coach.username}_{self.start_date}'
