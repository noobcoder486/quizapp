import pyotp
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    email_confirmed = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=32, default=pyotp.random_base32())

    def get_otp_object(self):
         otp = pyotp.TOTP(self.secret_key, interval=300)
         return otp

    def verify_otp(self, input_otp):
          self.email_confirmed = self.get_otp_object().verify(input_otp)
          self.save()
          return self.email_confirmed

    def send_otp(self):
         otp = self.get_otp_object()
         send_mail(
            'Sign Up One Time OTP',
            otp.now(),
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently = False,
        )

          


