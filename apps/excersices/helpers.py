from .models import *
def get_fields_excersice_history_pass_to_only(user):
        excersice_history_fields=[f.name for f in Excersice_history._meta.get_fields()]
        excersice_fields=['excersice__name','excersice__status']
        athlete_fields=['excersice__sport_history__athlete__username']
        coach_fields=[]
        if user.role=='athlete':
            athlete_fields.append('excersice__sport_history__athlete__public_id')
        elif user.role=='coach':coach_fields.append('excersice__sport_history__coach__public_id')
        fields_pass_to_only=excersice_history_fields+excersice_fields+athlete_fields+coach_fields
        return fields_pass_to_only


def get_fields_excersice_pass_to_only(params):
        include=params.get('include')      
        excersice_fields=[f.name for f in Excersice._meta.get_fields()]
        raw_history_fields=[f.name for f in Excersice_history._meta.get_fields() ] if include and 'history' in include else['public_id']
        history_fields = ['excersice_history__'+f.name for f in Excersice_history._meta.get_fields()] \
                            if include and 'history' in include else ['excersice_history__public_id']
        realted_fields=['sport_history__coach__public_id','sport_history__athlete__public_id'
                        ,'excersice_history__excersice__public_id']
        fields_pass_to_only=excersice_fields+history_fields+realted_fields
        return fields_pass_to_only,history_fields,raw_history_fields