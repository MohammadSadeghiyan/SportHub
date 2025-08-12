import jdatetime
import datetime
from rest_framework import serializers

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
    


    
