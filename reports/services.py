from users.models import MidUser,Manager
from training.models import Reservation
from orders.models import Order,MembershipItem
from memberships.models import Membership
from decimal import Decimal
from django.db.models import Prefetch
from payments.models import RecpetionistPayment
from .helpers import set_start_date
from .models import Report
def count_active_user(start_date):
    active_user=MidUser.objects.filter(last_login__gte=start_date).exclude(role='receptionist')\
                                                                        .filter(memberships__status=True)\
                                                                            .distinct().count()
    return active_user

def count_inactive_user(start_date):

    inactive_user=0
    inactive_user=MidUser.objects.filter(last_login__lt=start_date).exclude(role='receptionist')\
                                                                .exclude(memberships__status=True)\
                                                                    .distinct().count()
    return inactive_user

def count_expired_user(start_date,end_date):
    expired_user=0
    expired_user=MidUser.objects.filter(date_joined__gte=start_date,date_joined__lte=end_date).exclude(role='receptionist')\
                                                                                                .exclude(memberships__status=True)\
                                                                                                    .distinct().count()
    return expired_user

def count_total_reserve(start_date,end_date):
    total_rervers_count=Reservation.objects.filter(date__gte=start_date,date__lte=end_date).count()
    return total_rervers_count

def calculate_total_sale(start_date,end_date):
    membership_order_items=MembershipItem.objects.filter(order__status='paid')\
                                                    .filter(order__registered_at__gte=start_date,order__registered_at__lte=end_date)\
                                                        .values('order','price')
    total=Decimal(0)

    membership_orders=[]
    for membership_item in membership_order_items:
        membership_orders.append(membership_item['order'])
        total+=membership_item['price']



    orders_price=Order.objects.exclude(pk__in=membership_orders).filter(status='paid')\
                                                                    .filter(registered_at__gte=start_date,registered_at__lte=end_date)\
                                                                         .values_list('price',flat=True)
    for price in orders_price:
        total+=price*.1

    return total

def calculate_total_payment(start_date,end_date):
    price_payments=RecpetionistPayment.objects.filter(date__gte=start_date,date__lte=end_date).values_list('salary',flat=True)
    if not price_payments:return Decimal(0) 
    return Decimal(sum(price_payments))

def calculate_report_data(start_date,end_date):
    output={}
    
    output['active_user']=count_active_user(start_date)

    output['inactive_user']=count_inactive_user(start_date)
   
    output['expired_user']=count_expired_user(start_date,end_date)
   
    output['total_reserve']=count_total_reserve(start_date,end_date)
    
    output['total_sale']=calculate_total_sale(start_date,end_date)
   
    output['total_payment']=calculate_total_payment(start_date,end_date)

    

    return output


def make_report(validated_data,user):

    end_date=validated_data['end_date']
    name=validated_data['name']
    type_name=validated_data['type_name']
    start_date=set_start_date(end_date=end_date,type_name=type_name)
    other_data=calculate_report_data(start_date,end_date)
    report=Report(**other_data,start_date=start_date,end_date=end_date,name=name,type_name=type_name)
    report.save()
    manager=Manager.objects.filter(pk=user.pk).first()
    manager.reports.add(report)
    manager.save()
    return report


def update_report(validated_data,instance,user):
        flag=False
        end_date=validated_data.get('end_date',instance.end_date)
        name=validated_data.get('name',instance.name)
        type_name=validated_data.get('type_name',instance.type_name)
        if end_date!=instance.end_date or type_name!=instance.type_name:
            flag=True
            if end_date:instance.end_date=end_date
            if type_name:instance.type_name=type_name
            start_date=set_start_date(end_date=instance.end_date,type_name=instance.type_name)
            instance.start_date=start_date
            other_data=calculate_report_data(start_date,instance.end_date)
            for field_name, value in other_data.items():
                setattr(instance, field_name, value)
        if name:
            flag=True
            instance.name=name
            
        if flag:instance.save()
        return instance