import imp
from unittest.mock import DEFAULT
import pyotp
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    secret_key=models.CharField(max_length=32,default=pyotp.random_base32())
