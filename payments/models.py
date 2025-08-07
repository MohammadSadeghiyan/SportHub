from django.db import models
from users.models import MidUser,Receptionist
from orders.models import Order

# Create your models here.

class Payment(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','failed')
    ]
    user = models.ForeignKey(MidUser, on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.DecimalField(max_digits=9, decimal_places=0,blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending',blank=True)
    
    tracking_code = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,related_name='payments')


    def __str__(self):
        return f'{self.user.username}_{self.tracking_code}'


class RecpetionistPayment(models.Model):
    user=models.ForeignKey(Receptionist,on_delete=models.SET_NULL,null=True,related_name='specific_payments')
    date=models.DateTimeField(auto_now_add=True)
    salary=models.DecimalField(max_digits=9,decimal_places=0)