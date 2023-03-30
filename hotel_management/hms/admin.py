from django.contrib import admin
from .models import *
from django.utils.html import format_html



class CustomBooking(admin.ModelAdmin):
    list_display = ['id','user', 'room' , 'check_in_date', 'check_out_date']
    list_display_links = ['id','user']


class CustomComment(admin.ModelAdmin):
    list_display = ['id','user', 'room', 'email']
    list_display_links = ['id','user']


class CustomRoom(admin.ModelAdmin):
    # def thumbnail(self, object):
    #     return format_html('<img src="{}" width="50px" style="border-radius: 50%; " />'.format(object.image.url))

    # thumbnail.short_description = "Room photo"
    # list_display = ['thumbnail', 'room_no', 'room_status', 'room_type', 'beds', 'price']
    list_display = ['room_no', 'room_status', 'room_type', 'beds', 'price']
    list_display_links = ['room_no']


admin.site.register(Room, CustomRoom)
admin.site.register(Booking, CustomBooking)
admin.site.register(Comment, CustomComment)