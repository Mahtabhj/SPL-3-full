from django.contrib import admin

from wafrworkload.models import Region, AWSManagedService, Workload, Pillar

admin.site.register([Region, AWSManagedService, Workload, Pillar])
