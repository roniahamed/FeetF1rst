from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, OTP
from useraccount.utils.email import send_verification_email
from django.template.loader import render_to_string

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_email_verification(sender, instance, created, *args, **kwargs):
    if created and not instance.is_verified:
        subject = 'FeetF1rst OTP Verification'
        otp = OTP.generate_otp_code()
        html_message = render_to_string('email/email_verification.html', {'user': instance, 'otp': otp, 'full_name': instance.full_name})

        OTP.objects.create(user=instance, code=otp, purpose='email_verification')

        send_verification_email(subject = subject, user=instance.email, html_template=html_message)