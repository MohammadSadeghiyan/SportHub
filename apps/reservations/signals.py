from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from apps.orders.models import Order,ReservationItem

@receiver(post_save,sender=Reservation)
def handel_order_and_order_item(sender,instance,created,**kwargs):
        athlete=instance.athlete
        pended_order=Order.objects.filter(user=athlete,status='pending')
        if pended_order.exists():
            pended_order=pended_order.first()
            pended_order.price+=instance.salary_rial
            pended_order.save()
        else:
            pended_order=Order.objects.create(user=athlete,price=instance.salary_rial)
            
       
        ReservationItem.objects.create(order=pended_order,reservation=instance,price=instance.salary_rial)
        