from rest_framework.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

def MembershipOnlyfields():
    return ['start_date','end_date','type_name','status','user','membership_cost_rial','user__public_id']

def set_end_date(start_date,type_name):
    if type_name=='month':start_date=start_date+relativedelta(months=1)
    elif type_name=='year':start_date=start_date+relativedelta(years=1)
    else : raise ValidationError('your type name is not validate')
    return start_date
