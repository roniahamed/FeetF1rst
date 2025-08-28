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

def sent_otp_email(subject, email, user, otp, html_template):
    subject = 'FeetF1rst OTP Verification'
    html_message = render_to_string(html_template, {'user': user, 'otp': otp})
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email
    send_mail(subject, from_email, [to], html_message=html_message)
