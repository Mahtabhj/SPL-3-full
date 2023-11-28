# Generated by Django 4.1.6 on 2023-03-22 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wafrcloudaccount', '0002_alter_awsaccount_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AWSManagedService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'AWSManagedServices',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Regions',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Workload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('environment', models.CharField(max_length=100)),
                ('review_type', models.CharField(blank=True, default='Well-Architected Framework Review(WAFR)', max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('aws_account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='aws_account_workload', to='wafrcloudaccount.awsaccount')),
                ('aws_managed_services', models.ManyToManyField(blank=True, related_name='managed_service_workload', to='wafrworkload.awsmanagedservice')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='workload_created_by', to=settings.AUTH_USER_MODEL)),
                ('regions', models.ManyToManyField(blank=True, related_name='region_workload', to='wafrworkload.region')),
            ],
            options={
                'verbose_name_plural': 'Workloads',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Pillar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('workload', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pillar_workload', to='wafrworkload.workload')),
            ],
            options={
                'verbose_name_plural': 'Pillars',
                'ordering': ('created',),
            },
        ),
    ]