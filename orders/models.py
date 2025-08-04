from django.db import models
from users.models import MidUser
from users.models import SportHistory
from training.models import Reservation
from plans.models import NutritionPlan
from memberships.models import Membership
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','failed')
    ]
    user=models.ForeignKey(MidUser,on_delete=models.CASCADE,related_name='orders')
    created_at=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=7,choices=STATUS_CHOICES,default='pending')


class AbstractOrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=15, decimal_places=0,blank=True)
    
    class Meta:
        abstract = True

class SportHistoryItem(AbstractOrderItem):
    sporthistory=models.ForeignKey(SportHistory,on_delete=models.CASCADE,related_name='orders')

class MembershipItem(AbstractOrderItem):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE,related_name='orders')

class NutritionPlanItem(AbstractOrderItem):
    plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE,related_name='orders')

class ReservationItem(AbstractOrderItem):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='orders')

