from .models import WorkHistory

def get_work_history_only_fields():
    fields=[f.name for f in WorkHistory._meta.get_fields() ]+['user__public_id','user__username']
    return fields
