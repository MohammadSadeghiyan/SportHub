from .models import RecpetionistPayment,WithdrawalRequest,Payment
from rest_framework import serializers
from apps.djalalidates.serializers import JalaliDateField
from apps.receptionists.models import Receptionist
from apps.basicusers.models import MidUser

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='payment:payment-detail',lookup_field='public_id',read_only=True)
    user=serializers.SerializerMethodField()
    created_date=JalaliDateField(read_only=True)
    class Meta:
        model=Payment
        fields=['url','user','public_id','amount','status','order','tracking_code','created_date','created_time']
        read_only_fields=('url','user','public_id','amount','status','order','tracking_code','created_date','created_time')


    def get_user(self,obj):
        request=self.context.get('request')
        
        if obj.user.role=='athlete':
            return request.build_absolute_uri(f'/api/athletes/{obj.user.public_id}')
        return request.build_absolute_uri(f'/api/coaches/{obj.user.public_id}')
    
class ReceptionistPaymentSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='payment:receptionist-payment-detail',lookup_field='public_id',read_only=True)
    user_url=serializers.HyperlinkedRelatedField(source='user',view_name='receptionists:receptionist-detail',lookup_field='public_id',read_only=True)
    user=serializers.SlugRelatedField(slug_field='username',queryset=Receptionist.objects.all())
    created_date=JalaliDateField(read_only=True)
    updated_date=JalaliDateField(read_only=True)
    class Meta:
        model=RecpetionistPayment
        fields=['url','public_id','user_url','user','created_date','created_time','updated_date','updated_time','salary']
        read_only_fields=('url','public_id','created_date','created_time','updated_date','updated_time','user')
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        user=self.context.get('request').user

        if user.role=='receptionist':
            self.fields['salary'].read_only=True
            self.fields['user'].read_only=True


class WithdrawalRequestSerializer(serializers.HyperlinkedModelSerializer):

    url=serializers.HyperlinkedIdentityField(view_name='payment:withdrawalrequest-detail',lookup_field='public_id',read_only=True)
    user_url=serializers.SerializerMethodField()
    user=serializers.SlugRelatedField(slug_field='username',queryset=MidUser.objects.all())
    created_date=JalaliDateField(read_only=True)
    class Meta:
        model=WithdrawalRequest
        fields=['url','public_id','created_date','created_time','user_url','paid_date','paid_time','status','amount','user']
        read_only_fields=('url','public_id','created_date','created_time','user_url')
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        user=self.context.get('request').user

        if user.role=='user':
            self.fields['status'].read_only=True
            self.fields['paid_date'].read_only=True
            self.fields['paid_time'].read_only=True
    
    def get_user(self,obj):
        request=self.context.get('request')
        if obj.user.role=='athlete':
            return request.build_absolute_uri(f'/api/athletes/{obj.user.public_id}')
        return request.build_absolute_uri(f'/api/coaches/{obj.user.public_id}')
    
    def validate(self,data):
        user_request=self.context.get('request').user
        if user_request:
            user=data['user']
        else:
            user=MidUser.objects.get(public_id=user_request.public_id)
        
        if user.balance_rial<data['amount']:
            raise serializers.ValidationError({'amount isnt true':'your amount that you want is greater than your balance'})

