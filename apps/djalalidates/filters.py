from rest_framework.exceptions import ValidationError
import jdatetime
def filter_date(queryset,name,value):
            if not value:
                return queryset
            try:
                if value.count('/')!=2:
                    raise ValidationError('date must be have this format yyyy/mm/dd')
                date=value.split('/')
                if len(date[0])!=4 or len(date[1])!=2 or len(date[2])!=2:
                    raise ValidationError('date must be have this format yyyy/mm/dd')
                year, month, day = map(int, date)
                j_date = jdatetime.date(year, month, day)
                g_date = j_date.togregorian()
                
            except Exception as e:
                 raise ValidationError(f'date is invalid{e}')
            
            lookup=name
            return queryset.filter(**{lookup:g_date})