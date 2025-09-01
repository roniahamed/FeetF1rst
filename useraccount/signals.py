from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, OTP
from useraccount.utils.email import send_verification_email
from django.template.loader import render_to_string
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.core.files.base import ContentFile
import requests 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_email_verification(sender, instance, created, *args, **kwargs):
    if created and not instance.is_verified and instance.has_usable_password():
        subject = 'FeetF1rst OTP Verification'
        otp = OTP.generate_otp_code()
        html_message = render_to_string('email/email_verification.html', {'user': instance, 'otp': otp, 'full_name': instance.full_name})

        OTP.objects.create(user=instance, code=otp, purpose='email_verification')

        send_verification_email(subject = subject, email=instance.email, html_template=html_message)


@receiver([social_account_added, social_account_updated])
def update_profile_from_social(sender, request, sociallogin, *args, **kwargs):
    if sociallogin.account.provider == 'google':
        user = sociallogin.user 
        extra_data = sociallogin.account.extra_data

        picture_url = extra_data.get('picture', '')

        if picture_url:
            try: 
                profile, created = Profile.objects.get_or_create(user = user)

                if not profile.image:
                    response = requests.get(picture_url)

                    if response.status_code == 200:

                        file_name = f"{user.id}_google_profile.jpg"
                        profile.image.save(file_name, ContentFile(response.content), save=True)

            except Exception as e:
                pass
