from allauth.account.adapter import DefaultAccountAdapter
from rest_framework import status
from rest_framework.response import Response
from allauth.exceptions import ImmediateHttpResponse

class CustomAccountAdapter(DefaultAccountAdapter):
    
    def respond_user_inactive(self, request, user):

        return Response({"detail": "User account is inactive."}, status=status.HTTP_403_FORBIDDEN)