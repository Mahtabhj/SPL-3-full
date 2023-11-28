from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth import get_user_model
from wafrcloudaccount.models import AwsAccount

User = get_user_model()


class Region(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name


class AWSManagedService(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'AWSManagedServices'

    def __str__(self):
        return self.name


class Workload(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    aws_account = models.ForeignKey(AwsAccount, on_delete=models.DO_NOTHING, related_name='aws_account_workload')
    environment = models.CharField(max_length=100)
    regions = models.ManyToManyField(Region, related_name='region_workload', blank=True)
    aws_managed_services = models.ManyToManyField(AWSManagedService, related_name='managed_service_workload', blank=True)
    review_type = models.CharField(max_length=100, null=True, blank=True,
                                   default="Well-Architected Framework Review(WAFR)")
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='workload_created_by', blank=True,
                                   null=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Workloads'

    def __str__(self):
        return self.name


class Pillar(TimeStampedModel):
    name = models.CharField(max_length=100)
    workload = models.ForeignKey(Workload, on_delete=models.DO_NOTHING, related_name='pillar_workload')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Pillars'

    def __str__(self):
        return self.name
