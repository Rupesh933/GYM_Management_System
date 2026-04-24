from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# class CustomUserAdmin(userAdmin):
#     models = User
#     list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
#     fieldsets = userAdmin.fieldsets + (
#         ('role', {'fields' : ('role',)})
#     )
# OR
class UserAdmin(BaseUserAdmin):    # BaseUserAdmin = Special admin for User   and when You extend AbstractUser
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields':('role',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']

class MemberProfileAdmin(admin.ModelAdmin):   # ModelAdmin = Normal admin for any model
    list_display = ['full_name', 'user', 'mobile', 'join_date']
    search_fields = ['full_name', 'user__username', 'mobile']
    list_filter = ['plan', 'join_date']

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'contact_info', 'message', 'created_at', 'status']
    search_fields = ['name', 'email', 'contact_info']
    list_filter = ['status', 'created_at']
    

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(MemberShipPlan)
admin.site.register(Trainer)
admin.site.register(MemberProfile, MemberProfileAdmin)
admin.site.register(Equipment)
admin.site.register(Payment)
admin.site.register(Attendance)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(WorkoutPlan)
admin.site.register(Feedback)