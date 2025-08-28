from allauth.account.adapter import DefaultAccountAdapter
from rest_framework import status
from rest_framework.response import Response
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