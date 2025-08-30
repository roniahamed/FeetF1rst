from django.contrib.auth.backends import ModelBackend
from .models import User
from django.core.exceptions import ValidationError

class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        if not user.is_verified:
            raise ValidationError("Your email is not verified. Please verify your email to log in.")

        if not user.is_active:
            raise ValidationError("Your account is inactive. Please activate your account first or contact support.")
        
        return user