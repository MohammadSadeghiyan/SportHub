def nutritionplan_only_fields():
    return ['public_id','id','name','start_date','end_date','confirmation_coach','athlete__public_id','coach__public_id','created_at','salary_rial',
            'registered_at','status']

def meal_only_fields():
    return ['day','athlete_done','athlete_date_done','athlete_description','nutrtition_plan__public_id'
                    ,'nutrition__athlete__public_id','nutrition_plan__coach__public_id','public_id','id','meal_type',
                                                                           'athlete_discription','meal_discription']