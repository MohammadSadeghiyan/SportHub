from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class User(AbstractUser):
    class Meta:
        abstract = True
        
    USER_TYPE_CHOICES = (
        ("receptionist", _("Receptionist")),
        ("coache", _("Coache")),
        ("manager", _("Manager")),
        ("athlete",_("Athelete"))
    )
    user_type = models.CharField(max_length=13, choices=USER_TYPE_CHOICES, default="athlete")
    created_at=models.DateField(verbose_name=_("your first register"),auto_now_add=True)
    membership_start_date=models.DateField(verbose_name=_("member ship start date"),null=True)
    membership_end_date=models.DateField(verbose_name=_("membership end date"),null=True)
    balance_rial=models.DecimalField(verbose_name=_("balance(rial)"),max_digits=15,decimal_places=0)




    