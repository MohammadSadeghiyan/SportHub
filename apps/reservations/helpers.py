def reservation_only_fields():
    return ['id','public_id','status','registered_date','date','class_ref__public_id','athlete__public_id','reserved_by__public_id',
                          'salary_rial']