from datetime import timedelta


def class_only_fields():
    return ['public_id','name','session__public_id','coach__public_id','start_date','start_time','end_date','end_time',
                                    'capacity','class_salary_get_per_athlete_rial','days']


def count_class_days(start_date, end_date, days):
    days_of_week = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}
    target_weekdays = [days_of_week[d] for d in days]
    current = start_date
    count = 0
    while current <= end_date:
        if current.weekday() in target_weekdays:
            count += 1
        current += timedelta(days=1)
    return count
