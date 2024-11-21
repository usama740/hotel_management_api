from django.contrib import admin
from .models import User, Reservation, Menu

# Register models
admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(Menu)
