from .models import SportHistory
def coach_sport_history_serializer_read_only_fields():
    fields=['coach','start_date','end_date','athlete']
    return fields

def make_uri_excersice(obj,request):
    excersices=obj.excersices.all()
    return  [
                     request.build_absolute_uri(f'/api/excersices/{excersice.public_id}')
                     for excersice in excersices
            ]

def athlete_sport_history_serializer_read_only_fields():
    fields=['confirmation_coach','athlete']
    return fields


def sport_history_queryset_only_fields(excersice=None):
    fields=[]
    if excersice:
        fields=['excersices__public_id']
    fields+=[f.name for f in SportHistory._meta.get_fields()]+['athlete__public_id','athlete__balance_rial','coach__public_id',
                                                              'coach__balance_rial']
    return fields