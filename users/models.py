from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings


class User(AbstractUser):
    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=16, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# class User(AbstractUser):
#     username = models.CharField(max_length=30, blank=True, null=True)
#     email = models.EmailField(unique=True)
#     confirmation_code = models.CharField(max_length=16, blank=True, null=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return "{}".format(self.email)

# class UserProfile(models.Model):
#     USER_ROLES = (
#         ('user', 'user'),
#         ('moderator', 'moderator'),
#         ('admin', 'admin'),
#     )
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     first_name = models.CharField(max_length=200, blank=True)
#     last_name = models.CharField(max_length=200, blank=True)
#     username = models.SlugField(blank=True, null=True, unique=True)
#     role = models.CharField(max_length=10, choices=USER_ROLES)
#     bio = models.TextField(blank=True, null=True)
