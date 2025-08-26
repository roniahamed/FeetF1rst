from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User  # import your User model
        fields = ('id', 'email', 'full_name', 'dob', 'role', 'is_active', 'is_staff', 'date_joined')

class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Remove username field
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(max_length=255)
    dob = serializers.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  # Remove username field

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['full_name'] = self.validated_data.get('full_name', '')
        data['dob'] = self.validated_data.get('dob', '')
        return data