import logging
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

from wafrcloudaccount.models import AwsAccount
from wafrcloudaccount.serializers import AwsAccountSerializer, AwsAccountCreateSerializer
logger = logging.getLogger(__name__)
User = get_user_model()


class AwsAccountViewSet(viewsets.ModelViewSet):
    queryset = AwsAccount.objects.all()
    serializer_classes = {
        'retrieve': AwsAccountSerializer,
        'update': AwsAccountCreateSerializer,
        'partial_update': AwsAccountSerializer,
    }
    default_serializer_class = AwsAccountSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = AwsAccountCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
