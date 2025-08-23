from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from apps.orders.models import Order

@receiver(post_save,sender=Payment)
def update_order_statu(sender,instance,created,**kwargs):
    order= Order.objects.get(public_id=instance.order.public_id)
    order.status=instance.status
    order.save()

    
    for item in order.sporthistoryitem_items.all():
        if instance.status=='paid':
            status='r'
        else:status='nr'
        item.sporthistory.status=status
        item.sporthistory.save()
    
    for item in order.reservationitem_items.all():
        if instance.status=='paid':
            status='ack'
        else:status='wait'

        item.reservation.status=status
        item.reservation.save()
    
    for item in order.nutritionplanitem_items.all():
        if instance.status=='paid':
            status='r'
        else:status='nr'
        item.plan.status=status
        item.plan.save()

    for item in order.membershipitem_items.all():
        if instance.status=='paid':
            status=True
        else :status=False

        item.membership.status_activation=status

        item.membership.save()
