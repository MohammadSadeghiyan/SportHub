from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import SportHistory
from apps.orders.models import Order,SportHistoryItem
@receiver(post_save,sender=SportHistory)
def handel_order_and_order_item(sender, instance, created, **kwargs):
    if created :
        athlete=instance.athlete
        pended_order=Order.objects.filter(user=athlete,status='pending')
        if pended_order.exists():
            pended_order=pended_order.first()
            pended_order.price+=instance.balance_for_coaching_rial
            pended_order.save()
        else:pended_order=Order.objects.create(user=athlete,price=instance.balance_for_coaching_rial)
        SportHistoryItem.objects.create(order=pended_order,sporthistory=instance,price=instance.balance_for_coaching_rial)

    else:
        pended_orders=Order.objects.filter(user__public_id=instance.athlete.public_id,status='pending')
        pended_order=pended_orders.first()
        pended_order.price+=instance.membership_cost_rial
        pended_order.save()
        sporthistory=SportHistory.objects.get(sporthistory=instance,order=pended_order)
        sporthistory.price=instance.balance_for_coaching_rial
        sporthistory.save()
    
            
    