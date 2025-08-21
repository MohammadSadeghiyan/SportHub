from django.db import models
from apps.basicusers.models import MidUser
from django.core.validators import MinValueValidator
from shortuuidfield import ShortUUIDField
# Create your models here.

class Membership(models.Model):
    MEMBERSHIP_CHOICES=[
        ('year','Year'),
        ('month','Month')
    ]
    STATUS_CHOICES=(
        ('ns','not start'),
        ('s','start'),
        ('f','finished')
    )
    public_id=ShortUUIDField(editable=False,unique=True)
    user=models.ForeignKey(MidUser,on_delete=models.SET_NULL,null=True,related_name='memberships')
    status_activation=models.BooleanField(default=False)
    status=models.CharField(max_length=2,choices=STATUS_CHOICES,default='ns')
    type_name=models.CharField(max_length=5,choices=MEMBERSHIP_CHOICES)
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(blank=True,null=True)
    membership_cost_rial=models.DecimalField(verbose_name='membership cost(rial)',max_digits=9,decimal_places=0,
                                             blank=True,validators=[MinValueValidator(0)])


    def __str__(self):
        return f'{self.user.username}_{self.status}'
