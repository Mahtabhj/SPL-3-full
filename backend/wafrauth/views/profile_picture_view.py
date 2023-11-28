from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from wafrauth.models import UserProfile
from wafrauth.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from urllib.parse import unquote


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'userprofile'):
            x_forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO', '')
            print(f"X-Forwarded-Proto: {x_forwarded_proto}")
            profile = request.user.userprofile
            if hasattr(profile, 'profile_picture') and profile.profile_picture:
                media_url = request.build_absolute_uri(
                    settings.MEDIA_URL + unquote(str(profile.profile_picture)))
                return Response({
                    'image_url': media_url,
                    'x_forwarded_proto': x_forwarded_proto
                })
            else:
                media_url = request.build_absolute_uri(
                    settings.MEDIA_URL + "profile_pictures/default.jpg")
                return Response({
                    "image_url": media_url,
                    'x_forwarded_proto': x_forwarded_proto

                })
        else:
            media_url = request.build_absolute_uri(
                settings.MEDIA_URL + "profile_pictures/default.jpg")
            return Response({
                "image_url": media_url,
                'x_forwarded_proto': x_forwarded_proto,

            })

    def post(self, request):
        data = request.data.copy()

        if hasattr(request.user, 'userprofile'):
            profile = request.user.userprofile
            data['user'] = request.user.id
            serializer = UserProfileSerializer(profile, data=data)

        else:
            # Update profile with uploaded image
            data['user'] = request.user.id
            serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
