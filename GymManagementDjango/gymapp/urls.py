from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('admin-login/', admin_login_view, name='admin_login'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin-logout/', admin_logout_view, name='admin_logout'),

    # Admin Membership Plan URLs
    path('admin_plans/', admin_plans_list, name='admin_plans_list'),
    path('admin_plans_add/', admin_plan_form, name='admin_plans_add'),
    path('admin_plan_edit/<int:plan_id>/', admin_plan_edit, name='admin_plan_edit'),
    path('admin_plan_delete/<int:plan_id>/', admin_plan_delete, name='admin_plan_delete'),

    # Admin trainer URLs
    path('admin_trainers/', admin_trainers_list, name='admin_trainers_list'),
    path('admin_trainers_add/', admin_trainers_add, name='admin_trainers_add'),
    path('admin_trainers_edit/<int:trainer_id>/', admin_trainers_edit, name='admin_trainers_edit'),
    path('admin_trainers_delete/<int:trainer_id>/', admin_trainers_delete, name='admin_trainers_delete'),

    # Member URLs
    path('admin_member/', admin_member_list, name='admin_member_list'),
    path('admin_member_add/', admin_member_add, name='admin_member_add'),
    path('admin_member_edit/<int:member_id>/', admin_member_edit, name='admin_member_edit'),
    path('admin_member_delete/<int:member_id>/', admin_member_delete, name='admin_member_delete'),

    path('check_username/', check_username, name='check_username'),
]