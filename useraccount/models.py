from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random, string, datetime 
from django.utils import timezone 
from django.conf import settings 
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, dob = None, password=None, role='customer', **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, full_name, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('partner', 'Partner'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

class OTP(models.Model):
    PURPOSE_CHOICES = (
        ("email_verification", "Email Verification"),
        ("login", "Login"),
        ("password_reset", "Password Reset"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    resend_count = models.IntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=2)
    
    @staticmethod
    def generate_otp_code(length=6):
        return ''.join(random.choices(string.digits, k=length))
    
    def __str__(self):
        return f"OTP for {self.user.email} - {self.purpose}"


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True,  storage=MediaCloudinaryStorage() )
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} Profile"


class ProfileOnboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_where = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    health_condition = models.CharField(max_length=255, blank=True, null=True)
    onboard_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Onboarding for {self.user.email}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_and_house_number = models.CharField(max_length=255)
    additional_address = models.CharField(
        max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Italy')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"
