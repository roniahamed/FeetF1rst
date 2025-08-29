from django.urls import path 
from .views import EmailVerifyResetOtp, VerifyEmailOTPView, SendPasswordResetOTPView


urlpatterns = [
    path('verify-email/', VerifyEmailOTPView.as_view(), name='verify_email'),
    path('resent-verify-email-otp/', EmailVerifyResetOtp.as_view(), name='resent_otp'),
    path('password-rest-otp/', SendPasswordResetOTPView.as_view(), name='password_rest_otp'),

]