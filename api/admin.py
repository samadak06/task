from django.contrib import admin
from .models import LuggageType,Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','Items','booked_by','total_price']



class LuggageTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','status']


class userProfileAdmin(admin.ModelAdmin):
    list_display = ['user','user_type','maximum_booking']

# admin.site.register(userProfile,userProfileAdmin)
admin.site.register(Booking,BookingAdmin)

admin.site.register(LuggageType,LuggageTypeAdmin)

#