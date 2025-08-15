import jdatetime
import datetime
from rest_framework import serializers

class JalaliDateField(serializers.DateField):
    def to_internal_value(self, data):
        if not data:
            return None
        try:
            if isinstance(data, str):
                if '/' in data:  
                    year, month, day = map(int, data.split('/'))
                    if year < 1500:  
                        j_date = jdatetime.date(year, month, day)
                        return j_date.togregorian()
                    else:  
                        return super().to_internal_value(data)
                elif '-' in data:  
                    year, month, day = map(int, data.split('-'))
                    if year < 1500:  
                        j_date = jdatetime.date(year, month, day)
                        return j_date.togregorian()
                    else:
                        return super().to_internal_value(data)
                else:
                    raise serializers.ValidationError("Invalid date format")
            elif isinstance(data, datetime.date):
                return data
            else:
                raise serializers.ValidationError("Invalid date type")
        except Exception as e:
            raise serializers.ValidationError(f"date is not ok: {e}")

    def to_representation(self, value):
        if isinstance(value, datetime.date):
            j_date = jdatetime.date.fromgregorian(date=value)
            return j_date.strftime('%Y/%m/%d')
        return value
