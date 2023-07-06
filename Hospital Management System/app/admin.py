from django.contrib import admin
from .models import *

class UserWithUserTypeAdmin(admin.ModelAdmin):
    list_filter=('role', 'specialist_in')
    list_display=('id','username','gender')

admin.site.register(UserWithUserType, UserWithUserTypeAdmin)
admin.site.register(Appointment)
admin.site.register(Feedback)