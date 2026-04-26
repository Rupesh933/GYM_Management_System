from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('admin-login/', admin_login_view, name='admin_login'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin-logout/', admin_logout_view, name='admin_logout'),
    path('admin_plans/', admin_plans_list, name='admin_plans_list'),
    path('admin_plans_add/', admin_plan_form, name='admin_plans_add'),
    path('admin_plan_edit/<int:plan_id>/', admin_plan_edit, name='admin_plan_edit'),
    path('admin_plan_delete/<int:plan_id>/', admin_plan_delete, name='admin_plan_delete'),
]