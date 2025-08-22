from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import MembershipItem, NutritionPlanItem, SportHistoryItem, ReservationItem
from .helpers import order_is_empty

@receiver(post_delete, sender=MembershipItem)
@receiver(post_delete, sender=NutritionPlanItem)
@receiver(post_delete, sender=SportHistoryItem)
@receiver(post_delete, sender=ReservationItem)
def handle_order_after_item_delete(sender, instance, **kwargs):
    order = instance.order


    if not order:
        return
    print(order)
    order.price -= instance.price

    if order_is_empty(order):
        order.delete()
    else:
        order.save()
