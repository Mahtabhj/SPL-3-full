from django.core.mail import send_mail

def send_email(subject, message, email_from, email):
    send_mail(subject, message, email_from, [email])
