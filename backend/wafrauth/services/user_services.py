import random
from django.conf import settings
from ..models import User, PasswordReset
from ..emails import send_email


class UserService:

    @staticmethod
    def send_otp_for_user_registration(email):
        subject = 'Your account verification email'
        otp = random.randint(100000, 999999)
        message = f'Your otp is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        send_email(subject, message, email_from, email)
        user_object = User.objects.get(email=email)
        user_object.otp = otp
        user_object.save()

    @staticmethod
    def send_otp_for_password_reset(email):
        subject = 'Your password reset OTP'
        otp = random.randint(100000, 999999)
        message = f'Your otp is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        send_email(subject, message, email_from, email)
        user = User.objects.get(email=email)
        PasswordReset.objects.create(user=user, code=otp)

