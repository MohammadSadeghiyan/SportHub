from django.db import models
from apps.mysessions.models import Mysession
from django.core.validators import MinValueValidator
from shortuuidfield import ShortUUIDField
# Create your models here.
class AbstractPricing(models.Model):
    public_id=ShortUUIDField(editable=False,unique=True)
    start_start_date=models.DateField()
    end_start_date=models.DateField()
    gym_fee = models.DecimalField(decimal_places=0, max_digits=12, default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        abstract=True

class MembershipPricing(AbstractPricing):
    MEMBERSHIP_TYPE=[
        ('year','Year'),
        ('month','Month')
    ]
    type_name=models.CharField(max_length=5,choices=MEMBERSHIP_TYPE)
    price=models.DecimalField(decimal_places=0,max_digits=12,blank=True,validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.public_id}_{self.type_name}'

class NutritionPricing(AbstractPricing):
    price_per_day=models.DecimalField(max_digits=12,decimal_places=0,validators=[MinValueValidator(0)])
  
    def __str__(self):
        return f'{self.public_id}'
    
class SportHistoryPricing(AbstractPricing):
    price_per_day=models.DecimalField(max_digits=12,decimal_places=0,validators=[MinValueValidator(0)])
    

    def __str__(self):
        return f'{self.public_id}'

class ClassPricing(models.Model):
    public_id=ShortUUIDField(editable=False,unique=True)
    session_ref=models.ManyToManyField(Mysession,through='ClassItemPricing',related_name='picing')

    def __str__(self):
        return f'{self.public_id}'
    
class ClassItemPricing(AbstractPricing):
    pricing=models.ForeignKey(ClassPricing,on_delete=models.CASCADE,related_name='items')
    session_ref=models.ForeignKey(Mysession,on_delete=models.SET_NULL,null=True,related_name='pricingitems')
    min_capacity=models.PositiveSmallIntegerField()
    max_capacity=models.PositiveSmallIntegerField()
    price_per_hour=models.DecimalField(decimal_places=0,max_digits=12,blank=True,validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.public_id}'