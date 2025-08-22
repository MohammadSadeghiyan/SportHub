from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Membership
from apps.orders.models import MembershipItem,Order


@receiver(post_save,sender=Membership)
def handle_order_and_order_item(sender,instance,created,**kwargs):
    if created:
        orders=Order.objects.filter(user__public_id=instance.user.public_id,status='pending')
        if orders.exists():
            order=orders.first()
            order.price+=instance.membership_cost_rial
            order.save()
        else:
            user=instance.user
            order=Order.objects.create(user=user,price=instance.membership_cost_rial)
        MembershipItem.objects.create(membership=instance,order=order,price=instance.membership_cost_rial)

    else:
        pended_orders=Order.objects.filter(user=user,status='pending')
        pended_order=pended_orders.first()
        pended_order.price+=instance.membership_cost_rial
        pended_order.save()
        membership=MembershipItem.objects.get(membership=instance,order=pended_order)
        membership.price=instance.membership_cost_rial
        membership.save()


