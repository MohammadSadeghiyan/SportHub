from django.contrib import admin
from .models import BaseUser,MidUser
# Register your models here.
admin.site.register(BaseUser)
admin.site.register(MidUser)