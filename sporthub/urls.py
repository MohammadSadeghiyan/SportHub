from django.contrib import admin
from django.urls import path,include
from . import api



urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('',include(api)),





]
