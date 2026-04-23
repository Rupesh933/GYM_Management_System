from django.db import models
from django.contrib.auth.models import AbstractUser   # Import AbstractUser for custom User model
from django.utils import timezone
from django.conf import settings  # Import settings to access AUTH_USER_MODEL

# Create your models here.


class User(AbstractUser):    # username, email, password, first_name, last_name, are inherited from AbstratUser
    ROLE_CHOICE = [
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='MEMBER')    # To determine whether the currently logged-in user is an Admin user or a Member user.

    def __str__(self):
        return f'{self.username} {self.role}'

class MemberShipPlan(models.Model):
    name = models.CharField(max_length=100)
    duration_months = models.PositiveIntegerField()   # eg: 1, 2, 3, 6, 12 months
    fee = models.DecimalField(max_digits=6, decimal_places=2)  # eg: 499.50
    description = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.duration_months} month - ${self.fee}'

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    specialization = models.CharField(max_length=200)
    shift_timings = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.specialization}'

class MemberProfile(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,   # Delete profile if user is deleted
                                 related_name='member_profile'  # Access profile via user.member_profile
                                 )
    full_name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(blank=True)
    join_date = models.DateField(default=timezone.now)
    plan = models.ForeignKey(MemberShipPlan,
                              on_delete=models.SET_NULL,    # if plan is deleted set to null
                              null=True, blank=True)
    memberShip_start = models.DateField(null=True, blank=True)
    memberShip_end = models.DateField(null=True, blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return f'{self.full_name} - {self.user.username}'
    
class Equipment(models.Model):
    name = models.CharField(max_length=100)  # Treadmill, Dumbbells
    units = models.PositiveIntegerField(default=1)  # eg: 5 treadmill, 7 dumbbells
    is_active = models.BooleanField(default=True)   # if removed/sold, mark as inactive instead of deleting record

    def __str__(self):
        return f"{self.name} (units: {self.units})"

class Payment(models.Model):
    PAYMENT_MODE_CHOICES = (
        ('CASH', 'Cash'),
        ('ONLINE', 'Online')
    )
    PAYMENT_STATUS_CHOICES = (
        ('PAID', 'Paid'),
        ('PENDING', 'Pending')
    )
    member = models.ForeignKey(MemberProfile, 
                               on_delete=models.CASCADE,  # if member is deleted, delete payment
                               related_name='payments',  # Access payment via member.payment
                               null=True, blank=True
                               )
    plan = models.ForeignKey(MemberShipPlan, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # eg: 2343.00
    payment_date = models.DateField(default=timezone.now)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES, null=True, blank=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='PENDING')  # 
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Payment of ${self.amount} by {self.member.full_name if self.member else "No Member"}'

class Attendance(models.Model):
    member = models.ForeignKey(MemberProfile,
                                on_delete=models.CASCADE,  # if member is deleted, delete Attendance record
                                related_name='attendances'  # Access Attendances via member.attendances
                               )
    date = models.DateField(default=timezone.now)   # Date of Attendance
    time_in = models.TimeField(null=True, blank=True)   # Time when member checked in

    class Meta:
        unique_together = ('member', 'date')    # Ensure one attendance record per member per day

    def __str__(self):
        return f'{self.member.full_name} - {self.date} - {self.time_in}'

class Enquiry(models.Model):
    ENQUIRY_STATUS_CHOICES = (
        ('NEW', 'New'),
        ('SEEN', 'Seen'),
        ('RESOLVED', 'Resolved')
    )
    name = models.CharField(max_length=100)  # Name of the person making the enquiry
    email = models.EmailField()  # Email Address for contact
    contact_info = models.BigIntegerField()
    message = models.TextField()  # The enquiry message 
    created_at = models.DateTimeField(auto_now_add=True)   # Timestamp when the enquiry
    status = models.CharField(max_length=50, choices=ENQUIRY_STATUS_CHOICES, default='NEW')

    def __str__(self):
        return f'Enquiry from {self.name} - {self.email}'

class WorkoutPlan(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE,   # if member is deleted, delete workout plan
                               related_name='workout_plans'  # Access workout plans via member.workout_plans
                               )
    title = models.CharField(max_length=100)  # Title of the workout plan
    description = models.TextField(blank=True)    # Description of the workout plan
    creation_at = models.DateTimeField(auto_now_add=True)  # TimeStamp when the workout plan

    def __str__(self):
        return f'{self.title} - created_at : {self.creation_at}'

class Feedback(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE,    # if member deleted, delete feedback
                               related_name='feedback'  # Access feedback via member.feedback
                               )
    message = models.TextField()   # feedback message from the user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.member.full_name} - created at: {self.created_at}'