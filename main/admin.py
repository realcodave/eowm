from django.contrib import admin
from .models import Rooms, Booking, Halls, Gallery, Profile, Payment
# Register your models here.

admin.site.register(Rooms)
admin.site.register(Booking)
admin.site.register(Halls)
admin.site.register(Gallery)
admin.site.register(Profile)
admin.site.register(Payment)