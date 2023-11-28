from rest_framework.serializers import ModelSerializer
from wafrworkload.models import Region, Pillar, AWSManagedService, Workload
from django.contrib.auth import get_user_model
from wafrauth.serializers import UserIdNameUsernameEmailSerializer
from wafrcloudaccount.serializers import AwsAccountIdNameSerializer

User = get_user_model()


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class AWSManagedServiceSerializer(ModelSerializer):
    class Meta:
        model = AWSManagedService
        fields = '__all__'


class AWSManagedServiceIdNameSerializer(ModelSerializer):

    class Meta:
        model = AWSManagedService
        fields = ('id', 'name',)


class RegionIdNameSerializer(ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'name',)


class WorkloadSerializer(ModelSerializer):
    aws_account = AwsAccountIdNameSerializer(read_only=True)
    regions = RegionIdNameSerializer(read_only=True,  many=True)
    aws_managed_services = AWSManagedServiceIdNameSerializer(read_only=True,  many=True)
    created_by = UserIdNameUsernameEmailSerializer(read_only=True)

    class Meta:
        model = Workload
        fields = '__all__'


class WorkloadCreateSerializer(ModelSerializer):
    class Meta:
        model = Workload
        fields = '__all__'


class WorkloadIdNameSerializer(ModelSerializer):

    class Meta:
        model = Workload
        fields = ('id', 'name',)


class PillarSerializer(ModelSerializer):
    workload = WorkloadIdNameSerializer(read_only=True)

    class Meta:
        model = Pillar
        fields = '__all__'


class PillarCreateSerializer(ModelSerializer):
    class Meta:
        model = Pillar
        fields = '__all__'
