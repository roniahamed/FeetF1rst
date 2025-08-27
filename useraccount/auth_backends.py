from django.contrib.auth.backends import ModelBackend
from .models import User
from django.core.exceptions import ValidationError

class EmailBackend(ModelBackend):
    def user_can_authenticate(self, user):
        if not user.is_active:
            raise ValidationError("Your account is inactive. Please activate your account first or contact support.")
        return user