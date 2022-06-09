import pyotp
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    email_confirmed = models.BooleanField(default=False)
    secret_key=models.CharField(max_length=32,default=pyotp.random_base32())
