from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SportHistory
from apps.orders.models import Order,SportHistoryItem
@receiver(post_save,sender=SportHistory)
def make_order_and_order_item(sender, instance, created, **kwargs):
    if created :
        athlete=instance.athlete
        order=Order.objects.create(user=athlete)
        SportHistoryItem.objects.create(order=order,sport_history=instance)
        return 
    
            