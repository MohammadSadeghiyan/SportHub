from django.urls import path
from azbankgateways.urls import az_bank_gateways_urls
from .views import go_to_gateway_view,callback_gateway_view
app_name='payment'

urlpatterns = [
    path("bankgateways/", az_bank_gateways_urls()),
    path('go-to-bank-getway/<str:order_public_id>',go_to_gateway_view,name='go-to-getway'),
    path('call-back',callback_gateway_view,name='callback_gateway_view')
]