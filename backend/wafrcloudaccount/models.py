from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class AwsAccount(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    arn_of_iam_role = models.CharField(max_length=100, unique=True)
    bucket_name = models.CharField(max_length=100)
    report_name = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100, null=True, blank=True)
    prefix_path = models.TextField(max_length=100)
    role_session_name = models.TextField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='account_added_by', blank=True,
                                   null=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'AwsAccounts'

    def __str__(self):
        return self.name

