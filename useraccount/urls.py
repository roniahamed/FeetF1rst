from django.urls import path 
from .views import EmailVerifyResetOtp, VerifyEmailOTPView


urlpatterns = [
    path('verify-email/', VerifyEmailOTPView.as_view(), name='verify_email'),
    path('resent-verify-email-otp/', EmailVerifyResetOtp.as_view(), name='resent_otp'),

]