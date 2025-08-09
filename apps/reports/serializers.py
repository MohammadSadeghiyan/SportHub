from rest_framework import serializers
from .models import Report
from rest_framework import serializers
import jdatetime
import datetime
from .helpers import date_validator
class JalaliDateField(serializers.DateField):
    def to_internal_value(self, data):
        try:
            if isinstance(data, str) and data.startswith('20'):
                return super().to_internal_value(data)
            year, month, day = map(int, data.split('/'))
            j_date = jdatetime.date(year, month, day)
            g_date = j_date.togregorian()
            return g_date 
        except Exception as e:
            raise serializers.ValidationError(f"date is not ok: {e}")

    def to_representation(self, value):
        
        if isinstance(value, datetime.date):
            j_date = jdatetime.date.fromgregorian(date=value)
            return j_date.strftime('%Y/%m/%d')
        return value

class ReportSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='reports:report-detail',read_only=True,lookup_field='pk')
    end_date=JalaliDateField()
    start_date=JalaliDateField(read_only=True)
    class Meta:
        model=Report
        fields='__all__'
        read_only_fields=[field.name for field in Report._meta.fields if field.name not in['type_name','end_date','name']]


    def validate_start_date(self,value):
        date_validator(value)
        return value

    def validate_end_date(self,value):
        date_validator(value)
        return value