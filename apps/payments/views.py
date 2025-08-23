import logging
from django.urls import reverse
from django.shortcuts import render
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException

import logging
from django.urls import reverse
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException

from apps.orders.models import Order
from .models import *
from rest_framework import viewsets,permissions,mixins,exceptions
from .serializers import *
from .permissions import *
from .filters import *

def go_to_gateway_view(request,order_public_id,balance_user,user_public_id):
    # خواندن مبلغ از هر جایی که مد نظر است
    if order_public_id:
        order=Order.objects.get(public_id=order_public_id)
        amount = order.price
    else:
        user=MidUser.objects.get(public_id=user_public_id)
        if -(user.balance_rial)>balance_user:
            amount=balance_user
        else :
            raise exceptions.ValidationError({'balnce isnt true':'you want to pay to the gym max than your negative balance . you cant do it'})
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    #user_mobile_number = "+989112221234"  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)

        # در صورت تمایل می توانید داده های دلخواه خود را به درگاه ارسال کنید
       # bank.set_custom_data({"foo": "bar"})


        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse("callback-gateway"))
        #bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()
        if order_public_id:
            payment=Payment.objects.create(order=order,user=order.user,amount=amount,tracking_code=bank_record.tracking_code,status="pending")
        else:
            payment=Payment.objects.create(user=user_public_id,amount=amount,tracking_code=bank_record.tracking_code,status="pending")

        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e
    

import logging

from django.http import HttpResponse, Http404
from django.urls import reverse

from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        payment = Payment.objects.get(tracking_code=tracking_code)
    except Payment.DoesNotExist:
        return HttpResponse("پرداخت یافت نشد.")
    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        payment.status = "paid"
        payment.save()
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return HttpResponse("پرداخت با موفقیت انجام شد.")
    
    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    else:
        payment.status = "failed"
        payment.save()
        return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
        )
    



class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    
    
    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptionist']:
            return Payment.objects.all().select_related('user','order')
        return Payment.objects.filter(user__public_id=user.public_id).select_related('user','order')
    
    serializer_class=PaymentSerializer
    filterset_class=PaymentFilter
    lookup_field='public_id'
    permission_classes=[permissions.IsAuthenticated,ManagerReceptionSelfUserReadOnly]
    


class ReceptionistPaymentViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user=self.request.user
        if user.role=='manager':
            return RecpetionistPayment.objects.all().select_related('user')
        return RecpetionistPayment.objects.filter(user__public_id=user.public_id).select_related('user')
    
    serializer_class=ReceptionistPaymentSerializer
    filterset_class=ReceptionistPaymentFilter
    permission_classes=[permissions.IsAuthenticated,ManagerOrReceptionistReadOnly]
    lookup_field='public_id'


    

class WithdrawalRequestViewSet(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin
                               ,viewsets.GenericViewSet):

    def get_queryset(self):
        user=self.request.user

        if user.role in ['manager','receptionist']:
            return WithdrawalRequest.objects.all().select_related('user')
        else:
            return WithdrawalRequest.objects.filter(user__public_id=user.public_id).select_related('user')
    
    serializer_class=WithdrawalRequestSerializer
    filterset_class=WithdrawalRequestFilter
    permission_classes=[permissions.IsAuthenticated,ManagerOrReceptionistOrSelfUser]
    lookup_field='public_id'

    def perform_create(self, serializer):
        user=self.request.user
        data=serializer.validated_data
        if user.role in ['manager','receptionist']:
            user=data.pop('user')
        else:user=MidUser.objects.get(public_id=user.public_id)
        WithdrawalRequest.objects.create(**serializers.validated_data,user=user)

    
