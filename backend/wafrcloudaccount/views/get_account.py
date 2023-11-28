from typing import Any
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import AwsAccount
from rest_framework.exceptions import ValidationError
from rest_framework import serializers


class AwsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwsAccount
        fields = '__all__'


class GetAccountView(APIView):
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get(self, request, format=None):
        query_params = request.query_params
        account_id = query_params.get('account_id')
        account = AwsAccount.objects.filter(name=account_id).first()
        if not account_id:
            raise ValidationError(
                {'account_id': 'This field is required.'})
        account = AwsAccount.objects.filter(name=account_id).first()
        if not account:
            raise ValidationError(
                {'account_id': 'Invalid account ID.'})
        serializer = AwsAccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
