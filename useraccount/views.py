from rest_framework.views import APIView
from rest_framework.response import Response 
from .models import OTP, User 
from rest_framework import status
from django.conf import settings
from django.template.loader import render_to_string 
from useraccount.utils.email import send_verification_email
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class VerifyEmailOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')
        user = None

        if not email:
            return Response({'error': 'Email is required'})
        if not otp_code:
            return Response({'error': 'OTP is required'})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_verified:
            return Response({"error": "User already verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = OTP.objects.filter(user = user, code = otp_code, is_used=False, purpose= 'email_verification').order_by('created_at').last()

        if not otp or otp.is_expired():
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        otp.is_used = True
        otp.save()
        otp.delete()
        user.is_verified = True
        user.is_active = True
        user.save()

        subject = 'Email Verified Successfully!'
        html_template = render_to_string('email/email_verification_successful.html', {'user': user,'full_name': user.full_name})

        send_verification_email(subject = subject, email = user.email ,html_template = html_template )
        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
    
class EmailVerifyResetOtp(APIView):

    def post(self, request):
        email = request.data.get('email')
        
        user = User.objects.filter(email = email).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_verified:
            return Response({"error": "User already verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        active_otp = OTP.objects.filter( Q(user__email=email) | Q(purpose='email_verification') | Q (is_used=False)).order_by('created_at').last()

        if active_otp and not active_otp.is_expired():
            return Response(
            {"error": "Already sent OTP, please try using the existing one."},
            status=status.HTTP_400_BAD_REQUEST
        )
        otp = OTP.generate_otp_code()

        OTP.objects.create(code = otp, user = user, purpose = 'email_verification')
        subject = 'FeetF1rst OTP Verification'
        html_template = render_to_string('email/email_verification.html', {'user': user, 'otp': otp, 'full_name': user.full_name})

        send_verification_email(subject = subject, email = user.email, html_template = html_template )

        return Response({"message": "OTP resent successfully."}, status=status.HTTP_200_OK)

        
class SendPasswordResetOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        user = User.objects.filter(email = email, is_verified = True).first()

        if not user:
            return Response({'error':"User not found or not verified"}, status = status.HTTP_400_BAD_REQUEST)
        
        active_otp = OTP.objects.filter(Q(user__email = email) | Q(purpose = 'password_reset') | Q(is_used=False)).order_by('created_at').last()

        if active_otp and not active_otp.is_expired():
             return Response(
            {"error": "Already sent OTP, please try using the existing one."},
            status=status.HTTP_400_BAD_REQUEST
        )
        
        otp = OTP.generate_otp_code()

        OTP.objects.create(code=otp, user=user, purpose = 'password_reset')

        subject = "FeetF1rst Password Reset OTP"
        html_template = render_to_string('email/password_reset_otp.html', {'user':user, 'otp':otp, 'full_name':user.full_name})

        send_verification_email(subject=subject, email=email, html_template= html_template)

        return Response({"message": " Password Reset OTP successfully."}, status=status.HTTP_200_OK)

class ResetPasswordWithOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response( {"error": "Both new password and confirm password are required."},status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response(
                {"error": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            validate_password(new_password)
        except ValidationError as e:
            return Response(
                {"error": list(e.messages)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        

        user = User.objects.filter(email=email, is_verified=True).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        otp = OTP.objects.filter(user=user, code=otp_code, purpose="password_reset", is_used=False).last()
        if not otp or otp.is_expired():
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        otp.is_used = True
        otp.save()

        return Response({"message": "Password reset successfully"})

