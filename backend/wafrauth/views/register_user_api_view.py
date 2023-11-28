from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wafrauth.serializers import CreateUserSerializer, VerifyUserSerializer
# from ..services.user_services import UserService
User = get_user_model()


class RegisterUserAPIView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = CreateUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # email = serializer.data['email']
                # UserService.send_otp_for_user_registration(email)
                return Response({
                    'status': 200,
                    'message': 'Registration Completed',
                    'data': serializer.data,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class VerifyOTP(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = VerifyUserSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response("Invalid Email", status=status.HTTP_400_BAD_REQUEST)
                if not user[0].otp == otp:
                    return Response("Wrong OTP", status=status.HTTP_400_BAD_REQUEST)
                user = user.first()
                user.is_verified = True
                user.otp = None
                user.save()

                return Response({
                    'status': 200,
                    'message': 'Account verified successfully',
                    'data': serializer.data,
                })

        except Exception as e:
            print(e)
