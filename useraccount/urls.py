from django.urls import path, include
from .views import EmailVerifyResetOtp, VerifyEmailOTPView, SendPasswordResetOTPView, ResetPasswordWithOTPView, GoogleLogin


urlpatterns = [
    path('verify-email/', VerifyEmailOTPView.as_view(), name='verify_email'),
    path('resent-verify-email-otp/', EmailVerifyResetOtp.as_view(), name='resent_otp'),
    path('password-rest-otp/', SendPasswordResetOTPView.as_view(), name='password_rest_otp'),
    path('password-rest/', ResetPasswordWithOTPView.as_view(), name='password_reset' ),
    path('social/', include('allauth.socialaccount.urls')),
    path('google/login/', GoogleLogin.as_view(), name='google_login'), 
    
]