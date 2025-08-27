from datetime import date
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User, Profile, ProfileOnboard, Address
from rest_framework.validators import UniqueValidator
from allauth.account import app_settings as allauth_account_settings 


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('image', 'gender', 'mobile', 'language', 'address')



class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User  # import your User model
        fields = ('id', 'email', 'full_name', 'dob', 'role', 'is_active', 'is_staff', 'date_joined')

class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Remove username field
    email = serializers.EmailField(required=allauth_account_settings.EMAIL_REQUIRED, validators=[UniqueValidator(queryset=User.objects.all())])
    full_name = serializers.CharField(max_length=255)
    dob = serializers.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  # Remove username field
    
    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("This email is already registered.")
    #     return value

    def validate_dob(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value


    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['full_name'] = self.validated_data.get('full_name', '')
        data['dob'] = self.validated_data.get('dob', '')
        return data
    
    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data.get('full_name')
        user.dob = self.cleaned_data.get('dob')
        user.is_active = False  # User must activate via email
        user.save()
        return user