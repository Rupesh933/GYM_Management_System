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
    role = models.CharFiled(max_length=20, choice=ROLE_CHOICE, default='MEMBER')    # To determine whether the currently logged-in user is an Admin user or a Member user.

    def __str__(self):
        return f'{self.username} {self.role}'

