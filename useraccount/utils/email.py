from django.core.mail import send_mail
from django.conf import settings 
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(user):
    subject = 'Welcome to Our Service!'
    html_message = render_to_string('welcome_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_verification_email(subject, email, user, otp, html_template, **kwargs):
    html_message = render_to_string(html_template, {'user': user, 'otp': otp, 'full_name': user.full_name})
    from_email = settings.DEFAULT_FROM_EMAIL
    from_email = settings.DEFAULT_FROM_EMAIL
    if not from_email:
        raise ValueError("DEFAULT_FROM_EMAIL is not set in settings.py")
    to = email
    recipient_list = [email]
    send_mail(subject,'', from_email, recipient_list, html_message=html_message, fail_silently=False)
