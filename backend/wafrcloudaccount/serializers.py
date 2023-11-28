from rest_framework.serializers import ModelSerializer, SerializerMethodField
from wafrcloudaccount.models import AwsAccount
from django.contrib.auth import get_user_model
from wafrauth.serializers import UserIdNameUsernameEmailSerializer

User = get_user_model()


class AwsAccountSerializer(ModelSerializer):
    created_by = UserIdNameUsernameEmailSerializer(read_only=True)

    class Meta:
        model = AwsAccount
        fields = '__all__'


class AwsAccountCreateSerializer(ModelSerializer):
    class Meta:
        model = AwsAccount
        fields = '__all__'


class AwsAccountIdNameSerializer(ModelSerializer):

    class Meta:
        model = AwsAccount
        fields = ('id', 'name',)

