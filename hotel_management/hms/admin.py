from django.contrib import admin
from .models import *


class CustomBooking(admin.ModelAdmin):
    list_display = ['id','user', 'room' , 'check_in_date', 'check_out_date']
    list_display_links = ['id','user']

admin.site.register(Room)
admin.site.register(Booking, CustomBooking)
