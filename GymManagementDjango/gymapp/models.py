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
    specilization = models.CharField(max_length=200)
    shift_timings = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.specilization}'

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
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    address = models.TextField(blank=True)
    join_date = models.DateField(default=timezone.now())
    plan = models.ForeingKey(MemberShipPlan,
                              on_deleted=models.SET_NULL,    # if plan is deleted set to null
                              null=True, blank=True)
    memberShip_start = models.DateField(null=True, blank=True)
    memberShip_end = models.DateField(null=True, blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True related_name='member')

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
        ('CASE', 'Case'),
        ('ONLINE', 'Online')
    )
    PAYMENT_STATUS_CHOICES = (
        ('PAID', 'Paid'),
        ('PENDING', 'Pending')
    )