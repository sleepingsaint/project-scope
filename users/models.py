from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def default_info():
    return {}

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    bio = models.TextField(null=True)
    info = models.JSONField(null=True, default=default_info) 