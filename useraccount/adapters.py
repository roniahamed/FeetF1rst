from allauth.account.adapter import DefaultAccountAdapter
from rest_framework import status
from rest_framework.response import Response
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User
from allauth.exceptions import ImmediateHttpResponse


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        user.full_name = data.get('full_name', '')
        user.dob = data.get('dob', None)
        if commit:
            user.save()
        return user
    
    def respond_user_inactive(self, request, user):

        return Response({"detail": "User account is inactive."}, status=status.HTTP_403_FORBIDDEN)
    
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):


    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '')

        if email and User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            if not user.is_active:
                response_data = {
                    "detail": "This user's account is inactive. Please contact support.",
                    "code": "account_inactive"
                }

                raise ImmediateHttpResponse(Response(response_data,status=status.HTTP_403_FORBIDDEN))
            
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)
        

    def save_user(self, request, sociallogin, form=None):

        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data 

        user.full_name = extra_data.get('name', '')
        
        user.is_verified = True
        user.save()
        return user
    

        
