from django.db import models
from apps.basicusers.models import MidUser
from apps.orders.models import Order
from apps.receptionists.models import Receptionist
from django.core.validators import MinValueValidator
from shortuuidfield import ShortUUIDField
# Create your models here.

class Payment(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','failed')
    ]
    public_id=ShortUUIDField(editable=False,unique=True)
    user = models.ForeignKey(MidUser, on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.DecimalField(max_digits=9, decimal_places=0,blank=True,validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending',blank=True)
    
    tracking_code = models.CharField(max_length=255, blank=True)
    created_date = models.DateField(auto_now_add=True)
    created_time=models.TimeField(auto_now_add=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,related_name='payments')


    def __str__(self):
        return f'{self.user.username}_{self.tracking_code}'


class RecpetionistPayment(models.Model):
    public_id=ShortUUIDField(editable=False,unique=True)
    user=models.ForeignKey(Receptionist,on_delete=models.SET_NULL,null=True,related_name='specific_payments')
    created_date=models.DateTimeField(auto_now_add=True)
    created_time=models.TimeField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    updated_time=models.TimeField(auto_now=True)
    salary=models.DecimalField(max_digits=9,decimal_places=0,validators=[MinValueValidator(0)])


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("rejected", "Rejected"),
        ("paid", "Paid"),  
    ]
    user=models.ForeignKey(MidUser,related_name='withdrawalrequests',on_delete=models.SET_NULL,null=True)
    public_id = ShortUUIDField(editable=False, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_date = models.DateField(auto_now_add=True)
    created_time=models.TimeField(auto_now_add=True)
    paid_date=models.DateField(null=True)
    paid_time=models.TimeField(null=True)
    def __str__(self):
        return f"Withdrawal {self.amount} from {self.wallet.user.username} ({self.status})"
