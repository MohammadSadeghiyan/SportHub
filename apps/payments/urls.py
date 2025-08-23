from django.urls import path,include
from azbankgateways.urls import az_bank_gateways_urls
from .views import go_to_gateway_view,callback_gateway_view
from rest_framework.routers import SimpleRouter
from .views import *
app_name='payment'

router=SimpleRouter()
router.register('recpetionist-payments',ReceptionistPaymentViewSet,'receptionist-payment')
router.register('withdrawalrequests',WithdrawalRequestViewSet,'withdrawalrequest')
router.register('payments',PaymentViewSet,'payment')

urlpatterns = [
    path("bankgateways/", az_bank_gateways_urls()),
    path('go-to-bank-getway/<str:order_public_id>/<int:balance_user>/<str:user_public_id>',go_to_gateway_view,name='go-to-getway'),
    path('call-back/',callback_gateway_view,name='callback_gateway_view'),
    path('',include(router.urls))
]