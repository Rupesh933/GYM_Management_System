from django.urls import path
from .views import *

urlpatterns = [
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("admin-login/", admin_login_view, name="admin_login"),
    path("admin-dashboard/", admin_dashboard_view, name="admin_dashboard"),
    path("admin-logout/", admin_logout_view, name="admin_logout"),
    # Admin Membership Plan URLs
    path("admin_plans/", admin_plans_list, name="admin_plans_list"),
    path("admin_plans_add/", admin_plan_form, name="admin_plans_add"),
    path("admin_plan_edit/<int:plan_id>/", admin_plan_edit, name="admin_plan_edit"),
    path(
        "admin_plan_delete/<int:plan_id>/", admin_plan_delete, name="admin_plan_delete"
    ),
    # Admin trainer URLs
    path("admin_trainers/", admin_trainers_list, name="admin_trainers_list"),
    path("admin_trainers_add/", admin_trainers_add, name="admin_trainers_add"),
    path(
        "admin_trainers_edit/<int:trainer_id>/",
        admin_trainers_edit,
        name="admin_trainers_edit",
    ),
    path(
        "admin_trainers_delete/<int:trainer_id>/",
        admin_trainers_delete,
        name="admin_trainers_delete",
    ),
    # Member URLs
    path("admin_member/", admin_member_list, name="admin_member_list"),
    path("admin_member_add/", admin_member_add, name="admin_member_add"),
    path(
        "admin_member_edit/<int:member_id>/",
        admin_member_edit,
        name="admin_member_edit",
    ),
    path(
        "admin_member_delete/<int:member_id>/",
        admin_member_delete,
        name="admin_member_delete",
    ),
    path("check_username/", check_username, name="check_username"),
    # Attendance URLs
    path("admin_attendance_list/", admin_attendance_list, name="admin_attendance_list"),
    path("admin_attendance_add/", admin_attendance_add, name="admin_attendance_add"),
    path(
        "admin_attendance_edit/<int:attendance_id>/",
        admin_attendance_edit,
        name="admin_attendance_edit",
    ),
    path(
        "admin_attendance_delete/<int:attendance_id>/",
        admin_attendance_delete,
        name="admin_attendance_delete",
    ),

    # Equipment URLs
    path('admin_equipment_list', admin_equipment_list, name='admin_equipment_list'),
    path('admin_equipment_add', admin_equipment_add, name='admin_equipment_add'),
    path('admin_equipment/<int:equipment_id>/edit/', admin_equipment_edit, name='admin_equipment_edit'),
    path('admin_equipment/<int:equipment_id>/delete/', admin_equipment_delete, name='admin_equipment_delete'),


    # Enquiry URLs
    path('admin_enquiry_list/', admin_enquiry_list, name='admin_enquiry_list'),
    path('admin_enquiry_list/<int:enquiry_id>/update_status/', admin_enquiry_update_status, name='admin_enquiry_update_status'),
    path('admin_enquiry_delete/<int:enquiry_id>/', admin_enquiry_delete, name='admin_enquiry_delete'),

    # Workout plans URLs
    path('admin_workout_plan_list/',admin_workout_plan_list, name='admin_workout_plan_list'),
    path('admin_workout_plans_add/', admin_workout_plan_add, name='admin_workout_plans_add'),
    path('admin_workout_plan_edit/<int:workout_plan_id>/', admin_workout_plan_edit, name='admin_workout_plan_edit'),
    path('admin_workout_plan_delete/<int:workout_plan_id>/', admin_workout_plan_delete, name='admin_workout_plan_delete'),

    # Payment URLs
    path('admin_payment_list/', admin_payment_list, name='admin_payment_list'),
    path('admin_payment_add_edit/', admin_payment_add, name='admin_payment_add_edit'),

    # Member URLs
    path('member-login/', member_login_view, name='member_login'),
    path('member-dashboard/', member_dashboard_view, name='member_dashboard'),
    path('member_attendance/', member_attendance_view, name='member_attendance'),
    path('member_membership/', member_membership, name='member_membership'),
    path('member_payment/', member_payment, name='member_payment'),
    path('member_workout_plans/', member_workout_plans, name='member_workout_plans'),
    path('member_profile/', member_profile, name='member_profile'),
    path('member_profile_edit/', member_profile_edit, name='member_profile_edit'),
    path('member_change_password/', member_change_password, name='member_change_password'),

    # member feedback
    path('member_feedback/', member_feedback, name='member_feedback'),
]
