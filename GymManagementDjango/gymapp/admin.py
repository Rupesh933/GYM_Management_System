from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(MemberShipPlan)
admin.site.register(Trainer)
admin.site.register(MemberProfile)
admin.site.register(Equipment)
admin.site.register(Payment)
admin.site.register(Attendance)