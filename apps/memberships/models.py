from django.db import models
from apps.basicusers.models import MidUser
from django.core.validators import MinValueValidator
# Create your models here.

class Membership(models.Model):
    membership_type=[
        ('year','Year'),
        ('month','Month')
    ]
    user=models.ForeignKey(MidUser,on_delete=models.SET_NULL,null=True,related_name='memberships')
    status=models.BooleanField(default=False)
    type=models.CharField(max_length=7,choices=membership_type)
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    membership_cost_rial=models.DecimalField(verbose_name='membership cost(rial)',max_digits=9,decimal_places=0,
                                             validators=[MinValueValidator(0)])


    def __str__(self):
        return f'{self.user.username}_{self.status}'
