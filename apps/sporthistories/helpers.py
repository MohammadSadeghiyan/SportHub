def coach_sport_history_serializer_read_only_fields():
    fields=['coach','start_date','end_date','athlete']
    return fields

def make_uri_excersice(obj,request):
    excersices=obj.excersices.all()
    return {
                    'excersices':[
                     request.build_absolute_uri(f'/api/excersices/{excersice.public_id}')
                     for excersice in excersices
            ]}

def athlete_sport_history_serializer_read_only_fields():
    fields=['coconfirmation_coach','athlete']
    return fields