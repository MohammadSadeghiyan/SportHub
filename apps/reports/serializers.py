from rest_framework import serializers
from .models import Report
from rest_framework import serializers
from .helpers import date_validator
from apps.djalalidates.serializers import JalaliDateField

class ReportSerializer(serializers.ModelSerializer):
    end_date=JalaliDateField()
    start_date=JalaliDateField(read_only=True)
    type_name_display=serializers.CharField(source='get_type_name_display',read_only=True)
    type_name=serializers.ChoiceField(write_only=True,choices=Report.TYPE_CHOICE)
    class Meta:
        model=Report
        fields = ['start_date','end_date','type_name_display']+[f.name for f in Report._meta.get_fields() if f.name not in ['id','manager']]
        read_only_fields=[field.name for field in Report._meta.fields if field.name not in['type_name','end_date','name']]

    def validate_start_date(self,value):
        date_validator(value)
        return value

    def validate_end_date(self,value):
        date_validator(value)
        return value